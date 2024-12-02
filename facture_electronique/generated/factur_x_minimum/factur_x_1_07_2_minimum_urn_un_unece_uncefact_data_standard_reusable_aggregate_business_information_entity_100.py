from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

from facture_electronique.generated.factur_x_minimum.factur_x_1_07_2_minimum_urn_un_unece_uncefact_data_standard_qualified_data_type_100 import (
    CountryIdtype,
    CurrencyCodeType,
    DocumentCodeType,
)
from facture_electronique.generated.factur_x_minimum.factur_x_1_07_2_minimum_urn_un_unece_uncefact_data_standard_unqualified_data_type_100 import (
    AmountType,
    DateTimeType,
    Idtype,
    TextType,
)

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"


class HeaderTradeDeliveryType(BaseModel):
    pass
    model_config = ConfigDict(defer_build=True)


class DocumentContextParameterType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class ExchangedDocumentType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    type_code: DocumentCodeType = field(
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    issue_date_time: DateTimeType = field(
        metadata={
            "name": "IssueDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class LegalOrganizationType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


class ReferencedDocumentType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    issuer_assigned_id: Idtype = field(
        metadata={
            "name": "IssuerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class TaxRegistrationType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: Idtype = field(
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class TradeAddressType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    country_id: CountryIdtype = field(
        metadata={
            "name": "CountryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class TradeSettlementHeaderMonetarySummationType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    tax_basis_total_amount: AmountType = field(
        metadata={
            "name": "TaxBasisTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    tax_total_amount: List[AmountType] = field(
        default_factory=list,
        metadata={
            "name": "TaxTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "max_occurs": 2,
        },
    )
    grand_total_amount: AmountType = field(
        metadata={
            "name": "GrandTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    due_payable_amount: AmountType = field(
        metadata={
            "name": "DuePayableAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class ExchangedDocumentContextType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    business_process_specified_document_context_parameter: Optional[
        DocumentContextParameterType
    ] = field(
        default=None,
        metadata={
            "name": "BusinessProcessSpecifiedDocumentContextParameter",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    guideline_specified_document_context_parameter: DocumentContextParameterType = field(
        metadata={
            "name": "GuidelineSpecifiedDocumentContextParameter",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class HeaderTradeSettlementType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    invoice_currency_code: CurrencyCodeType = field(
        metadata={
            "name": "InvoiceCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    specified_trade_settlement_header_monetary_summation: TradeSettlementHeaderMonetarySummationType = field(
        metadata={
            "name": "SpecifiedTradeSettlementHeaderMonetarySummation",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )


class TradePartyType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    name: TextType = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    specified_legal_organization: Optional[LegalOrganizationType] = field(
        default=None,
        metadata={
            "name": "SpecifiedLegalOrganization",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    postal_trade_address: Optional[TradeAddressType] = field(
        default=None,
        metadata={
            "name": "PostalTradeAddress",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_tax_registration: List[TaxRegistrationType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTaxRegistration",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "max_occurs": 2,
        },
    )


class HeaderTradeAgreementType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    buyer_reference: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "BuyerReference",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    seller_trade_party: TradePartyType = field(
        metadata={
            "name": "SellerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    buyer_trade_party: TradePartyType = field(
        metadata={
            "name": "BuyerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    buyer_order_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "BuyerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


class SupplyChainTradeTransactionType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    applicable_header_trade_agreement: HeaderTradeAgreementType = field(
        metadata={
            "name": "ApplicableHeaderTradeAgreement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    applicable_header_trade_delivery: HeaderTradeDeliveryType = field(
        metadata={
            "name": "ApplicableHeaderTradeDelivery",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
    applicable_header_trade_settlement: HeaderTradeSettlementType = field(
        metadata={
            "name": "ApplicableHeaderTradeSettlement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        }
    )
