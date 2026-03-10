from typing import Optional
import datetime

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    profile_picture: Mapped[Optional[str]] = mapped_column(Text)
    is_online: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    last_seen: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    conversations: Mapped[list['Conversations']] = relationship('Conversations', back_populates='users')
    user_sessions: Mapped[list['UserSessions']] = relationship('UserSessions', back_populates='user')
    calls: Mapped[list['Calls']] = relationship('Calls', back_populates='caller')
    conversation_participants: Mapped[list['ConversationParticipants']] = relationship('ConversationParticipants', back_populates='user')
    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='sender')
    message_status: Mapped[list['MessageStatus']] = relationship('MessageStatus', back_populates='user')


class Conversations(Base):
    __tablename__ = 'conversations'
    __table_args__ = (
        ForeignKeyConstraint(['created_by'], ['users.id'], name='conversations_created_by_fkey'),
        PrimaryKeyConstraint('id', name='conversations_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_type: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'private'::character varying"))
    created_by: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='conversations')
    calls: Mapped[list['Calls']] = relationship('Calls', back_populates='conversation')
    conversation_participants: Mapped[list['ConversationParticipants']] = relationship('ConversationParticipants', back_populates='conversation')
    messages: Mapped[list['Messages']] = relationship('Messages', back_populates='conversation')


class UserSessions(Base):
    __tablename__ = 'user_sessions'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='user_sessions_user_id_fkey'),
        PrimaryKeyConstraint('id', name='user_sessions_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    jwt_token: Mapped[Optional[str]] = mapped_column(Text)
    login_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    logout_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_sessions')


class Calls(Base):
    __tablename__ = 'calls'
    __table_args__ = (
        ForeignKeyConstraint(['caller_id'], ['users.id'], name='calls_caller_id_fkey'),
        ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='calls_conversation_id_fkey'),
        PrimaryKeyConstraint('id', name='calls_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(Integer)
    caller_id: Mapped[Optional[int]] = mapped_column(Integer)
    call_type: Mapped[Optional[str]] = mapped_column(String(20))
    call_status: Mapped[Optional[str]] = mapped_column(String(20))
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ended_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    caller: Mapped[Optional['Users']] = relationship('Users', back_populates='calls')
    conversation: Mapped[Optional['Conversations']] = relationship('Conversations', back_populates='calls')


class ConversationParticipants(Base):
    __tablename__ = 'conversation_participants'
    __table_args__ = (
        ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE', name='conversation_participants_conversation_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='conversation_participants_user_id_fkey'),
        PrimaryKeyConstraint('id', name='conversation_participants_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    joined_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    conversation: Mapped[Optional['Conversations']] = relationship('Conversations', back_populates='conversation_participants')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='conversation_participants')


class Messages(Base):
    __tablename__ = 'messages'
    __table_args__ = (
        ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE', name='messages_conversation_id_fkey'),
        ForeignKeyConstraint(['sender_id'], ['users.id'], name='messages_sender_id_fkey'),
        PrimaryKeyConstraint('id', name='messages_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    conversation_id: Mapped[Optional[int]] = mapped_column(Integer)
    sender_id: Mapped[Optional[int]] = mapped_column(Integer)
    message_text: Mapped[Optional[str]] = mapped_column(Text)
    message_type: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'text'::character varying"))
    file_url: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    conversation: Mapped[Optional['Conversations']] = relationship('Conversations', back_populates='messages')
    sender: Mapped[Optional['Users']] = relationship('Users', back_populates='messages')
    message_status: Mapped[list['MessageStatus']] = relationship('MessageStatus', back_populates='message')


class MessageStatus(Base):
    __tablename__ = 'message_status'
    __table_args__ = (
        ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='CASCADE', name='message_status_message_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='message_status_user_id_fkey'),
        PrimaryKeyConstraint('id', name='message_status_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'sent'::character varying"))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    message: Mapped[Optional['Messages']] = relationship('Messages', back_populates='message_status')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='message_status')
