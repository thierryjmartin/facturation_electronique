from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"


@dataclass
class AmountType:
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    currency_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "currencyID",
            "type": "Attribute",
        },
    )


@dataclass
class CodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class DateTimeType:
    date_time_string: Optional["DateTimeType.DateTimeString"] = field(
        default=None,
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
            "required": True,
        },
    )

    @dataclass
    class DateTimeString:
        value: str = field(
            default="",
            metadata={
                "required": True,
            },
        )
        format: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass
class Idtype:
    class Meta:
        name = "IDType"

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


@dataclass
class IndicatorType:
    indicator: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Indicator",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
            "required": True,
        },
    )


@dataclass
class PercentType:
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
        },
    )


@dataclass
class QuantityType:
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    unit_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "unitCode",
            "type": "Attribute",
        },
    )


@dataclass
class TextType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
