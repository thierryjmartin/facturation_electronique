from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"


class AllowanceChargeReasonCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class CountryIdtype(BaseModel):
    class Meta:
        name = "CountryIDType"

    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class CurrencyCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class DocumentCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class FormattedDateTimeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    date_time_string: "FormattedDateTimeType.DateTimeString" = field(
        metadata={
            "name": "DateTimeString",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
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


class PaymentMeansCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class TaxCategoryCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class TaxTypeCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class TimeReferenceCodeType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
