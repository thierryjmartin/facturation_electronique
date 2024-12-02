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


class BinaryObjectType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: bytes = field(
        metadata={
            "required": True,
            "format": "base64",
        }
    )
    mime_code: str = field(
        metadata={
            "name": "mimeCode",
            "type": "Attribute",
            "required": True,
        }
    )
    filename: str = field(
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class CodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    list_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "listID",
            "type": "Attribute",
        },
    )
    list_version_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "listVersionID",
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


class DateType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    date_string: "DateType.DateString" = field(
        metadata={
            "name": "DateString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
            "required": True,
        }
    )

    class DateString(BaseModel):
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


class IndicatorType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    indicator: bool = field(
        metadata={
            "name": "Indicator",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
            "required": True,
        }
    )


class PercentType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: Decimal = field(
        metadata={
            "required": True,
        }
    )


class QuantityType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: Decimal = field(
        metadata={
            "required": True,
        }
    )
    unit_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "unitCode",
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
