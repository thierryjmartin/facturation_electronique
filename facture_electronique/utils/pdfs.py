def convert_to_pdfa(input_pdf_path: str, output_pdfa_path: str):
    import ghostscript

    args = [
        "gs",  # Ghostscript command
        "-dPDFA=3",  # Enable PDF/A output
        "-dBATCH",  # Batch mode: no user interaction
        "-dNOPAUSE",  # No pause between pages
        "-dNOOUTERSAVE",  # Disable outer save level
        "-sColorConversionStrategy=UseDeviceIndependentColor",
        "-sDEVICE=pdfwrite",  # Set output device to pdfwrite
        "-dPDFACompatibilityPolicy=1",  # PDF/A-1b compliance policy
        f"-sOutputFile={output_pdfa_path}",  # Output file path
        input_pdf_path,  # Input PDF file
    ]

    # Convert arguments into bytes (required by the ghostscript module)
    gs_args = [arg.encode("utf-8") for arg in args]

    # Call Ghostscript with the arguments
    ghostscript.Ghostscript(*gs_args)


def sign_pdf(
    input_pdf_path: str,
    output_pdf_signed_path: str,
    key_path: str,
    cert_path: str,
    ca_chain_files: tuple = tuple(),
    key_passphrase: bytes = None,
):
    from pyhanko import stamp
    from pyhanko.sign import signers, fields
    from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

    signer = signers.SimpleSigner.load(
        key_path,
        cert_path,
        ca_chain_files=ca_chain_files,
        key_passphrase=key_passphrase,
    )

    with open(input_pdf_path, "rb") as f:
        w = IncrementalPdfFileWriter(f)
        fields.append_signature_field(
            w, sig_field_spec=fields.SigFieldSpec("Signature", box=(0, 0, 200, 60))
        )
        meta = signers.PdfSignatureMetadata(field_name="Signature")
        pdf_signer = signers.PdfSigner(
            meta,
            signer=signer,
            stamp_style=stamp.TextStampStyle(
                stamp_text="Signed by: %(signer)s\nTime: %(ts)s",
            ),
        )
        with open(output_pdf_signed_path, "wb") as outf:
            pdf_signer.sign_pdf(w, output=outf)
    return
