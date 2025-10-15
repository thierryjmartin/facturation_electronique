from dataclasses import dataclass, field
from typing import List, Optional

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

__NAMESPACE__ = (
    "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
)


@dataclass
class HeaderTradeDeliveryType:
    pass


@dataclass
class DocumentContextParameterType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class ExchangedDocumentType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    type_code: Optional[DocumentCodeType] = field(
        default=None,
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    issue_date_time: Optional[DateTimeType] = field(
        default=None,
        metadata={
            "name": "IssueDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class LegalOrganizationType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class ReferencedDocumentType:
    issuer_assigned_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "IssuerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TaxRegistrationType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TradeAddressType:
    country_id: Optional[CountryIdtype] = field(
        default=None,
        metadata={
            "name": "CountryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TradeSettlementHeaderMonetarySummationType:
    tax_basis_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "TaxBasisTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
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
    grand_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "GrandTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    due_payable_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "DuePayableAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class ExchangedDocumentContextType:
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
    guideline_specified_document_context_parameter: Optional[
        DocumentContextParameterType
    ] = field(
        default=None,
        metadata={
            "name": "GuidelineSpecifiedDocumentContextParameter",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class HeaderTradeSettlementType:
    invoice_currency_code: Optional[CurrencyCodeType] = field(
        default=None,
        metadata={
            "name": "InvoiceCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    specified_trade_settlement_header_monetary_summation: Optional[
        TradeSettlementHeaderMonetarySummationType
    ] = field(
        default=None,
        metadata={
            "name": "SpecifiedTradeSettlementHeaderMonetarySummation",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TradePartyType:
    name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
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


@dataclass
class HeaderTradeAgreementType:
    buyer_reference: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "BuyerReference",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    seller_trade_party: Optional[TradePartyType] = field(
        default=None,
        metadata={
            "name": "SellerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    buyer_trade_party: Optional[TradePartyType] = field(
        default=None,
        metadata={
            "name": "BuyerTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    buyer_order_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "BuyerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class SupplyChainTradeTransactionType:
    applicable_header_trade_agreement: Optional[HeaderTradeAgreementType] = field(
        default=None,
        metadata={
            "name": "ApplicableHeaderTradeAgreement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    applicable_header_trade_delivery: Optional[HeaderTradeDeliveryType] = field(
        default=None,
        metadata={
            "name": "ApplicableHeaderTradeDelivery",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    applicable_header_trade_settlement: Optional[HeaderTradeSettlementType] = field(
        default=None,
        metadata={
            "name": "ApplicableHeaderTradeSettlement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
