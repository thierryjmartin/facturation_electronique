from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"


class AmountType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: Decimal = field(
        metadata={
            "required": True,
        }
    )
    currency_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "currencyID",
            "type": "Attribute",
        },
    )


class DateTimeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    date_time_string: "DateTimeType.DateTimeString" = field(
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
            "required": True,
        }
    )

    class DateTimeString(BaseModel):
        model_config = ConfigDict(defer_build=True)
        value: str = field(
            default="",
            metadata={
                "required": True,
            },
        )
        format: str = field(
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )


class Idtype(BaseModel):
    class Meta:
        name = "IDType"

    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    scheme_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "schemeID",
            "type": "Attribute",
        },
    )


class TextType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
