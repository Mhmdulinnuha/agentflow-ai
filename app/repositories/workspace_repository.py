from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember

def create_workspace(
    db:Session,
    workspace: Workspace,
) -> Workspace:
    """
    Menambahkan workspace baru ke database.
    """
    db.add(workspace)
    db.flush()
    
    return workspace

def get_workspace_by_id(
    db:Session,
    workspace_id: int,
) -> Workspace | None:
    """
    Mencari workspace berdasarkan ID.
    """
    statement = select(Workspace).where(
        Workspace.id == workspace_id
    )
    return db.scalar(statement)

def get_workspace_by_slug(
    db: Session,
    slug: str,
) -> Workspace | None:
    """
    Mencari workspace berdasarkan slug.
    """

    statement = select(Workspace).where(
        Workspace.slug == slug
    )

    return db.scalar(statement)

    
def get_user_workspaces(
    db: Session,
    user_id: int,
) -> list[Workspace]:
    """
    Mengambil semua workspace yang diikuti user.
    """

    statement = (
        select(Workspace)
        .join(
            WorkspaceMember,
            WorkspaceMember.workspace_id == Workspace.id,
        )
        .where(WorkspaceMember.user_id == user_id)
        .order_by(Workspace.created_at.desc())
    )

    return list(db.scalars(statement).all())


def update_workspace(
    db: Session,
    workspace: Workspace,
    update_data: dict,
) -> Workspace:
    """
    Memperbarui informasi workspace.
    """

    for field, value in update_data.items():
        setattr(workspace, field, value)

    db.flush()

    return workspace


def delete_workspace(
    db: Session,
    workspace: Workspace,
) -> None:
    """
    Menghapus workspace dari database.
    """

    db.delete(workspace)
    db.flush()
