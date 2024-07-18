from typing import Optional, List

from sqlalchemy import JSON, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database_models.base import Base

DEFAULT_TOOLS_MODULE = "backend.tools"
COMMUNITY_TOOLS_MODULE = "community.tools"


class Tool(Base):
    __tablename__ = "tools"

    name: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    implementation_class_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, default="")
    parameter_definitions: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    default_tool_config: Mapped[Optional[dict]] = mapped_column(JSON)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    auth_implementation: Mapped[Optional[str]] = mapped_column(Text)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(Text)

    agent_tool_associations = relationship(
        "AgentToolAssociation", back_populates="tool"
    )

    __table_args__ = (UniqueConstraint("name", name="tool_name_uc"),)

    @property
    def is_available(self) -> bool:
        # Check if an agent has a deployment config set
        for agent_assoc in self.agent_tool_associations:
            if not agent_assoc.tool_config:
                continue
            if all(value != "" for value in agent_assoc.tool_config.values()):
                return True
        # if no agent has a deployment config set, check if the deployment has a default config
        if not self.default_tool_config:
            return False
        return all(value != "" for value in self.default_tool_config.values())

    @property
    def env_vars(self) -> List[str]:
        return (
            list(self.default_tool_config.keys())
            if self.default_tool_config
            else []
        )

    @property
    def implementation_class(self):
        from backend.model_deployments.utils import get_module_class

        if not self.implementation_class_name:
            return None
        cls = get_module_class(
            DEFAULT_TOOLS_MODULE, self.deployment_class_name
        )
        if not cls:
            cls = get_module_class(
                COMMUNITY_TOOLS_MODULE, self.deployment_class_name
            )

        return cls
