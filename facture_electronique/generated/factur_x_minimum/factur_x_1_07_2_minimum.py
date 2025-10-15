from dataclasses import dataclass, field
from typing import Optional

from facture_electronique.generated.factur_x_minimum.factur_x_1_07_2_minimum_urn_un_unece_uncefact_data_standard_reusable_aggregate_business_information_entity_100 import (
    ExchangedDocumentContextType,
    ExchangedDocumentType,
    SupplyChainTradeTransactionType,
)

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"


@dataclass
class CrossIndustryInvoiceType:
    exchanged_document_context: Optional[ExchangedDocumentContextType] = field(
        default=None,
        metadata={
            "name": "ExchangedDocumentContext",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        },
    )
    exchanged_document: Optional[ExchangedDocumentType] = field(
        default=None,
        metadata={
            "name": "ExchangedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        },
    )
    supply_chain_trade_transaction: Optional[SupplyChainTradeTransactionType] = field(
        default=None,
        metadata={
            "name": "SupplyChainTradeTransaction",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        },
    )


@dataclass
class CrossIndustryInvoice(CrossIndustryInvoiceType):
    class Meta:
        namespace = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
