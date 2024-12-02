from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

from generated.factur_x_1_07_2_en16931_urn_un_unece_uncefact_data_standard_reusable_aggregate_business_information_entity_100 import (
    ExchangedDocumentContextType,
    ExchangedDocumentType,
    SupplyChainTradeTransactionType,
)

__NAMESPACE__ = "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"


class CrossIndustryInvoiceType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    exchanged_document_context: ExchangedDocumentContextType = field(
        metadata={
            "name": "ExchangedDocumentContext",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        }
    )
    exchanged_document: ExchangedDocumentType = field(
        metadata={
            "name": "ExchangedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        }
    )
    supply_chain_trade_transaction: SupplyChainTradeTransactionType = field(
        metadata={
            "name": "SupplyChainTradeTransaction",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
            "required": True,
        }
    )


class CrossIndustryInvoice(CrossIndustryInvoiceType):
    class Meta:
        namespace = (
            "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
        )

    model_config = ConfigDict(defer_build=True)
