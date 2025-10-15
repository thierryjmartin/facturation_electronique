from dataclasses import dataclass, field
from typing import List, Optional

from facture_electronique.generated.factur_x_en16931.factur_x_1_07_2_en16931_urn_un_unece_uncefact_data_standard_qualified_data_type_100 import (
    AllowanceChargeReasonCodeType,
    CountryIdtype,
    CurrencyCodeType,
    DocumentCodeType,
    FormattedDateTimeType,
    PaymentMeansCodeType,
    ReferenceCodeType,
    TaxCategoryCodeType,
    TaxTypeCodeType,
    TimeReferenceCodeType,
)
from facture_electronique.generated.factur_x_en16931.factur_x_1_07_2_en16931_urn_un_unece_uncefact_data_standard_unqualified_data_type_100 import (
    AmountType,
    BinaryObjectType,
    CodeType,
    DateTimeType,
    DateType,
    Idtype,
    IndicatorType,
    PercentType,
    QuantityType,
    TextType,
)

__NAMESPACE__ = (
    "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
)


@dataclass
class CreditorFinancialAccountType:
    ibanid: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "IBANID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    account_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "AccountName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    proprietary_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ProprietaryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class CreditorFinancialInstitutionType:
    bicid: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "BICID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class DebtorFinancialAccountType:
    ibanid: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "IBANID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


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
class LegalOrganizationType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    trading_business_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "TradingBusinessName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class LineTradeDeliveryType:
    billed_quantity: Optional[QuantityType] = field(
        default=None,
        metadata={
            "name": "BilledQuantity",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class NoteType:
    content: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Content",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    subject_code: Optional[CodeType] = field(
        default=None,
        metadata={
            "name": "SubjectCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class ProcuringProjectType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class ProductCharacteristicType:
    description: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    value: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class ProductClassificationType:
    class_code: Optional[CodeType] = field(
        default=None,
        metadata={
            "name": "ClassCode",
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
        },
    )
    uriid: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "URIID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    line_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "LineID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    type_code: Optional[DocumentCodeType] = field(
        default=None,
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    attachment_binary_object: Optional[BinaryObjectType] = field(
        default=None,
        metadata={
            "name": "AttachmentBinaryObject",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    reference_type_code: Optional[ReferenceCodeType] = field(
        default=None,
        metadata={
            "name": "ReferenceTypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    formatted_issue_date_time: Optional[FormattedDateTimeType] = field(
        default=None,
        metadata={
            "name": "FormattedIssueDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class SpecifiedPeriodType:
    start_date_time: Optional[DateTimeType] = field(
        default=None,
        metadata={
            "name": "StartDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    end_date_time: Optional[DateTimeType] = field(
        default=None,
        metadata={
            "name": "EndDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class SupplyChainEventType:
    occurrence_date_time: Optional[DateTimeType] = field(
        default=None,
        metadata={
            "name": "OccurrenceDateTime",
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
class TradeAccountingAccountType:
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
    postcode_code: Optional[CodeType] = field(
        default=None,
        metadata={
            "name": "PostcodeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    line_one: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "LineOne",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    line_two: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "LineTwo",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    line_three: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "LineThree",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    city_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "CityName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    country_id: Optional[CountryIdtype] = field(
        default=None,
        metadata={
            "name": "CountryID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    country_sub_division_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "CountrySubDivisionName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeCountryType:
    id: Optional[CountryIdtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TradePaymentTermsType:
    description: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    due_date_date_time: Optional[DateTimeType] = field(
        default=None,
        metadata={
            "name": "DueDateDateTime",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    direct_debit_mandate_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "DirectDebitMandateID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeSettlementFinancialCardType:
    id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    cardholder_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "CardholderName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeSettlementHeaderMonetarySummationType:
    line_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "LineTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    charge_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "ChargeTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    allowance_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "AllowanceTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
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
    rounding_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "RoundingAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    total_prepaid_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "TotalPrepaidAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
class TradeSettlementLineMonetarySummationType:
    line_total_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "LineTotalAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class TradeTaxType:
    calculated_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "CalculatedAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    type_code: Optional[TaxTypeCodeType] = field(
        default=None,
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    exemption_reason: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "ExemptionReason",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    basis_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "BasisAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    category_code: Optional[TaxCategoryCodeType] = field(
        default=None,
        metadata={
            "name": "CategoryCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    exemption_reason_code: Optional[CodeType] = field(
        default=None,
        metadata={
            "name": "ExemptionReasonCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    tax_point_date: Optional[DateType] = field(
        default=None,
        metadata={
            "name": "TaxPointDate",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    due_date_type_code: Optional[TimeReferenceCodeType] = field(
        default=None,
        metadata={
            "name": "DueDateTypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    rate_applicable_percent: Optional[PercentType] = field(
        default=None,
        metadata={
            "name": "RateApplicablePercent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class UniversalCommunicationType:
    uriid: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "URIID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    complete_number: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "CompleteNumber",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class DocumentLineDocumentType:
    line_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "LineID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    included_note: Optional[NoteType] = field(
        default=None,
        metadata={
            "name": "IncludedNote",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    included_note: List[NoteType] = field(
        default_factory=list,
        metadata={
            "name": "IncludedNote",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeAllowanceChargeType:
    charge_indicator: Optional[IndicatorType] = field(
        default=None,
        metadata={
            "name": "ChargeIndicator",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    calculation_percent: Optional[PercentType] = field(
        default=None,
        metadata={
            "name": "CalculationPercent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    basis_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "BasisAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    actual_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "ActualAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    reason_code: Optional[AllowanceChargeReasonCodeType] = field(
        default=None,
        metadata={
            "name": "ReasonCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    reason: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    category_trade_tax: Optional[TradeTaxType] = field(
        default=None,
        metadata={
            "name": "CategoryTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeContactType:
    person_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "PersonName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    department_name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "DepartmentName",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    telephone_universal_communication: Optional[UniversalCommunicationType] = field(
        default=None,
        metadata={
            "name": "TelephoneUniversalCommunication",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    email_uriuniversal_communication: Optional[UniversalCommunicationType] = field(
        default=None,
        metadata={
            "name": "EmailURIUniversalCommunication",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeProductType:
    global_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "GlobalID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    seller_assigned_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "SellerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    buyer_assigned_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "BuyerAssignedID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    description: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    applicable_product_characteristic: List[ProductCharacteristicType] = field(
        default_factory=list,
        metadata={
            "name": "ApplicableProductCharacteristic",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    designated_product_classification: List[ProductClassificationType] = field(
        default_factory=list,
        metadata={
            "name": "DesignatedProductClassification",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    origin_trade_country: Optional[TradeCountryType] = field(
        default=None,
        metadata={
            "name": "OriginTradeCountry",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradeSettlementPaymentMeansType:
    type_code: Optional[PaymentMeansCodeType] = field(
        default=None,
        metadata={
            "name": "TypeCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    information: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Information",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    applicable_trade_settlement_financial_card: Optional[
        TradeSettlementFinancialCardType
    ] = field(
        default=None,
        metadata={
            "name": "ApplicableTradeSettlementFinancialCard",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    payer_party_debtor_financial_account: Optional[DebtorFinancialAccountType] = field(
        default=None,
        metadata={
            "name": "PayerPartyDebtorFinancialAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    payee_party_creditor_financial_account: Optional[CreditorFinancialAccountType] = (
        field(
            default=None,
            metadata={
                "name": "PayeePartyCreditorFinancialAccount",
                "type": "Element",
                "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            },
        )
    )
    payee_specified_creditor_financial_institution: Optional[
        CreditorFinancialInstitutionType
    ] = field(
        default=None,
        metadata={
            "name": "PayeeSpecifiedCreditorFinancialInstitution",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class LineTradeSettlementType:
    applicable_trade_tax: Optional[TradeTaxType] = field(
        default=None,
        metadata={
            "name": "ApplicableTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    billing_specified_period: Optional[SpecifiedPeriodType] = field(
        default=None,
        metadata={
            "name": "BillingSpecifiedPeriod",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_trade_allowance_charge: List[TradeAllowanceChargeType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_trade_settlement_line_monetary_summation: Optional[
        TradeSettlementLineMonetarySummationType
    ] = field(
        default=None,
        metadata={
            "name": "SpecifiedTradeSettlementLineMonetarySummation",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    additional_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "AdditionalReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    receivable_specified_trade_accounting_account: Optional[
        TradeAccountingAccountType
    ] = field(
        default=None,
        metadata={
            "name": "ReceivableSpecifiedTradeAccountingAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class TradePartyType:
    id: List[Idtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    global_id: List[Idtype] = field(
        default_factory=list,
        metadata={
            "name": "GlobalID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    name: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    description: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    defined_trade_contact: Optional[TradeContactType] = field(
        default=None,
        metadata={
            "name": "DefinedTradeContact",
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
    uriuniversal_communication: Optional[UniversalCommunicationType] = field(
        default=None,
        metadata={
            "name": "URIUniversalCommunication",
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
class TradePriceType:
    charge_amount: Optional[AmountType] = field(
        default=None,
        metadata={
            "name": "ChargeAmount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    basis_quantity: Optional[QuantityType] = field(
        default=None,
        metadata={
            "name": "BasisQuantity",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    applied_trade_allowance_charge: Optional[TradeAllowanceChargeType] = field(
        default=None,
        metadata={
            "name": "AppliedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    seller_tax_representative_trade_party: Optional[TradePartyType] = field(
        default=None,
        metadata={
            "name": "SellerTaxRepresentativeTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    seller_order_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "SellerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    contract_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "ContractReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    additional_referenced_document: List[ReferencedDocumentType] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_procuring_project: Optional[ProcuringProjectType] = field(
        default=None,
        metadata={
            "name": "SpecifiedProcuringProject",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class HeaderTradeDeliveryType:
    ship_to_trade_party: Optional[TradePartyType] = field(
        default=None,
        metadata={
            "name": "ShipToTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    actual_delivery_supply_chain_event: Optional[SupplyChainEventType] = field(
        default=None,
        metadata={
            "name": "ActualDeliverySupplyChainEvent",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    despatch_advice_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "DespatchAdviceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    receiving_advice_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "ReceivingAdviceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class HeaderTradeSettlementType:
    creditor_reference_id: Optional[Idtype] = field(
        default=None,
        metadata={
            "name": "CreditorReferenceID",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    payment_reference: Optional[TextType] = field(
        default=None,
        metadata={
            "name": "PaymentReference",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    tax_currency_code: Optional[CurrencyCodeType] = field(
        default=None,
        metadata={
            "name": "TaxCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    invoice_currency_code: Optional[CurrencyCodeType] = field(
        default=None,
        metadata={
            "name": "InvoiceCurrencyCode",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    payee_trade_party: Optional[TradePartyType] = field(
        default=None,
        metadata={
            "name": "PayeeTradeParty",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_trade_settlement_payment_means: List[TradeSettlementPaymentMeansType] = (
        field(
            default_factory=list,
            metadata={
                "name": "SpecifiedTradeSettlementPaymentMeans",
                "type": "Element",
                "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            },
        )
    )
    applicable_trade_tax: List[TradeTaxType] = field(
        default_factory=list,
        metadata={
            "name": "ApplicableTradeTax",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "min_occurs": 1,
        },
    )
    billing_specified_period: Optional[SpecifiedPeriodType] = field(
        default=None,
        metadata={
            "name": "BillingSpecifiedPeriod",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_trade_allowance_charge: List[TradeAllowanceChargeType] = field(
        default_factory=list,
        metadata={
            "name": "SpecifiedTradeAllowanceCharge",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    specified_trade_payment_terms: Optional[TradePaymentTermsType] = field(
        default=None,
        metadata={
            "name": "SpecifiedTradePaymentTerms",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
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
    invoice_referenced_document: List[ReferencedDocumentType] = field(
        default_factory=list,
        metadata={
            "name": "InvoiceReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    receivable_specified_trade_accounting_account: Optional[
        TradeAccountingAccountType
    ] = field(
        default=None,
        metadata={
            "name": "ReceivableSpecifiedTradeAccountingAccount",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )


@dataclass
class LineTradeAgreementType:
    buyer_order_referenced_document: Optional[ReferencedDocumentType] = field(
        default=None,
        metadata={
            "name": "BuyerOrderReferencedDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    gross_price_product_trade_price: Optional[TradePriceType] = field(
        default=None,
        metadata={
            "name": "GrossPriceProductTradePrice",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        },
    )
    net_price_product_trade_price: Optional[TradePriceType] = field(
        default=None,
        metadata={
            "name": "NetPriceProductTradePrice",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class SupplyChainTradeLineItemType:
    associated_document_line_document: Optional[DocumentLineDocumentType] = field(
        default=None,
        metadata={
            "name": "AssociatedDocumentLineDocument",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    specified_trade_product: Optional[TradeProductType] = field(
        default=None,
        metadata={
            "name": "SpecifiedTradeProduct",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    specified_line_trade_agreement: Optional[LineTradeAgreementType] = field(
        default=None,
        metadata={
            "name": "SpecifiedLineTradeAgreement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    specified_line_trade_delivery: Optional[LineTradeDeliveryType] = field(
        default=None,
        metadata={
            "name": "SpecifiedLineTradeDelivery",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )
    specified_line_trade_settlement: Optional[LineTradeSettlementType] = field(
        default=None,
        metadata={
            "name": "SpecifiedLineTradeSettlement",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "required": True,
        },
    )


@dataclass
class SupplyChainTradeTransactionType:
    included_supply_chain_trade_line_item: List[SupplyChainTradeLineItemType] = field(
        default_factory=list,
        metadata={
            "name": "IncludedSupplyChainTradeLineItem",
            "type": "Element",
            "namespace": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
            "min_occurs": 1,
        },
    )
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
