import re
from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.repositories import workspace_repository
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate

def generate_slug(name:str) -> str:
    """
    Mengubah nama workspace menjadi slug URL.
    Contoh: AgentFlow Development
    menjadi: agentflow-development
    """
    
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug =slug.strip("-")
    return slug

def create_workspace(
    db:Session,
    user_id:int,
    workspace_data: WorkspaceCreate,
) -> Workspace:
    """
    Membuat workspace baru dan menetapkan
    pembuatnya sebagai owner.
    """
    
    try:
        base_slug = generate_slug(workspace_data.name)
        slug = base_slug
        counter = 1
        
        while workspace_repository.get_workspace_by_slug(
            db,
            slug,
        ):
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        workspace = Workspace(
            name=workspace_data.name,
            slug=slug,
            description=workspace_data.description,
            created_by=user_id,
        )
        
        workspace_repository.create_workspace(
            db,
            workspace,
        )
        
        owner = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user_id,
            role="owner",
        )
        
        db.add(owner)
        db.commit
        db.refresh(workspace)
        return workspace
    except Exception:
        db.rollback()
        raise
    
def get_user_workspaces(
    db: Session,
    user_id: int,
) -> list[Workspace]:
    """
    Mengambil seluruh workspace yang
    diikuti pengguna.
    """

    return workspace_repository.get_user_workspaces(
        db,
        user_id,
    )


def get_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
) -> Workspace:
    """
    Mengambil workspace jika user merupakan anggota.
    """

    workspace = workspace_repository.get_workspace_by_id(
        db,
        workspace_id,
    )

    if not workspace:
        raise ValueError("Workspace tidak ditemukan")

    member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == user_id,
    ).first()

    if not member:
        raise PermissionError(
            "Kamu tidak memiliki akses ke workspace ini"
        )

    return workspace


def update_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
    workspace_data: WorkspaceUpdate,
) -> Workspace:
    """
    Mengubah workspace.
    Hanya owner dan admin yang boleh mengubah.
    """

    try:
        workspace = get_workspace(
            db,
            workspace_id,
            user_id,
        )

        member = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        ).first()

        if member.role not in ["owner", "admin"]:
            raise PermissionError(
                "Kamu tidak memiliki izin mengubah workspace"
            )

        update_data = workspace_data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            workspace.name = update_data["name"]
            base_slug = generate_slug(workspace.name)
            slug = base_slug
            counter = 1

            while (
                workspace_repository.get_workspace_by_slug(db, slug)
                and slug != workspace.slug
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1

            workspace.slug = slug

        if "description" in update_data:
            workspace.description = update_data["description"]

        db.commit()
        db.refresh(workspace)

        return workspace

    except Exception:
        db.rollback()
        raise


def delete_workspace(
    db: Session,
    workspace_id: int,
    user_id: int,
) -> None:
    """
    Menghapus workspace.
    Hanya owner yang boleh menghapus.
    """

    try:
        workspace = get_workspace(
            db,
            workspace_id,
            user_id,
        )

        member = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        ).first()

        if member.role != "owner":
            raise PermissionError(
                "Hanya owner yang boleh menghapus workspace"
            )

        workspace_repository.delete_workspace(
            db,
            workspace,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

