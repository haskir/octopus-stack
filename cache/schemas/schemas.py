from json import dumps

from lib.cache.schemas.abstract_scheme import AbstractScheme

from lib.models import *
from lib.utils import DateTimeUtils, day_in_seconds


class ParticipationScheme(AbstractScheme[ParticipationMessage]):
    model = ParticipationMessage
    key = "participation"

    @classmethod
    def get_key(cls, obj: ParticipationMessage):
        return f'{cls.key}:{obj.user_id}'

    @classmethod
    def dump(cls, obj: ParticipationMessage):
        return dumps(obj.model_dump(by_alias=True))

    @classmethod
    def expire(cls, obj: ParticipationMessage) -> int:
        return 60


class GiveawayScheme(AbstractScheme[Giveaway]):
    model = Giveaway
    key = "giveaway"

    @classmethod
    def get_key(cls, obj: Giveaway):
        return f'{cls.key}:{obj.id}'

    @classmethod
    def dump(cls, obj: Giveaway):
        return dumps(obj.model_dump(by_alias=True))

    @classmethod
    def expire(cls, obj: Giveaway) -> int:
        if obj.status == "POSTED":
            if obj.end_type == "TIME":
                # Небольшой костыль, чтобы отрицательные значения не получить
                return max(DateTimeUtils.seconds_until_datetime(obj.end_at), 1)
            else:
                return day_in_seconds
        return 60 * 10


class ChannelScheme(AbstractScheme[ChannelInfo]):
    model = ChannelInfo
    key = "channel"

    @classmethod
    def get_key(cls, obj: ChannelInfo):
        return f'{cls.key}:{obj.id}'

    @classmethod
    def dump(cls, obj: ChannelInfo):
        return dumps(obj.model_dump(by_alias=True))

    @classmethod
    def expire(cls, obj: ChannelInfo) -> int:
        return day_in_seconds


class GiveawayParticipantsScheme(AbstractScheme[GiveawayParticipants]):
    model = GiveawayParticipants
    key = "participants"

    @classmethod
    def get_key(cls, obj: GiveawayParticipants):
        return f'{cls.key}:{obj.id}'

    @classmethod
    def dump(cls, obj: GiveawayParticipants):
        return obj.to_json()

    @classmethod
    def expire(cls, obj: GiveawayParticipants) -> int:
        """ 10 минут """
        return 60 * 10


schemas: dict = {
    ParticipationMessage: ParticipationScheme,
    Giveaway: GiveawayScheme,
    ChannelInfo: ChannelScheme,
    GiveawayParticipants: GiveawayParticipantsScheme
}

__all__ = ["schemas"]
