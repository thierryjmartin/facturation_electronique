from dataclasses import dataclass, field

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:QualifiedDataType:100"


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
class DocumentCodeType:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
