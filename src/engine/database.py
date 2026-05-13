import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Float, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"

class RuleAction(enum.Enum):
    ALLOW = "allow" # Whitelist
    DENY = "deny"   # Blacklist

class TargetType(enum.Enum):
    IP = "ip"
    DOMAIN = "domain"
    SUBNET = "subnet"

class Verdict(enum.Enum):
    ALLOWED_BY_RULE = "allowed_by_rule"
    DENIED_BY_RULE = "denied_by_rule"
    ALLOWED_BY_AI = "allowed_by_ai"
    DENIED_BY_AI = "denied_by_ai"

class ReviewStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    """Usuários e Moderadores do sistema."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.MODERATOR, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    rules_created = relationship("FilteringRule", back_populates="author")
    reviews_resolved = relationship("ReviewRequest", back_populates="resolved_by_user")

class FilteringRule(Base):
    """Substitui as tabelas separadas de Whitelist/Blacklist por uma Tabela de Regras Unificada."""
    __tablename__ = "filtering_rules"

    id = Column(Integer, primary_key=True)
    target = Column(String(255), nullable=False, index=True) # IP, Subnet ou Domain
    target_type = Column(Enum(TargetType), nullable=False)
    action = Column(Enum(RuleAction), nullable=False) # ALLOW ou DENY
    reason = Column(Text, nullable=True)
    
    # Auditoria de quem adicionou essa regra
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    author = relationship("User", back_populates="rules_created")

class TrafficLog(Base):
    """Logs de tráfego ultra-rápidos"""
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True)
    source_ip = Column(String(50), nullable=False, index=True)
    destination_ip = Column(String(50), nullable=False, index=True)
    destination_domain = Column(String(255), nullable=True)
    port = Column(Integer, nullable=False)
    
    verdict = Column(Enum(Verdict), nullable=False)
    confidence_score = Column(Float, nullable=True) # Caso tenha sido decisão da IA
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class ReviewRequest(Base):
    """Feedback Loop: Solicitações de revisão para moderação humana."""
    __tablename__ = "review_requests"

    id = Column(Integer, primary_key=True)
    traffic_log_id = Column(Integer, ForeignKey("traffic_logs.id"), nullable=False)
    
    reporter_email = Column(String(100), nullable=True) 
    reason = Column(Text, nullable=False)
    
    status = Column(Enum(ReviewStatus), default=ReviewStatus.PENDING)
    
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    resolved_by_user = relationship("User", back_populates="reviews_resolved")

