from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"


@dataclass
class AccountingAccountTypeCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class AllowanceChargeReasonCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class ContactTypeCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class CountryIdtype:
    class Meta:
        name = "CountryIDType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class CurrencyCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class DeliveryTermsCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class DocumentCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class FormattedDateTimeType:
    date_time_string: Optional["FormattedDateTimeType.DateTimeString"] = field(
        default=None,
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
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
class LineStatusCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class PartyRoleCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class PaymentMeansCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class ReferenceCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class TaxCategoryCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class TaxTypeCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class TimeReferenceCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class TransportModeCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
