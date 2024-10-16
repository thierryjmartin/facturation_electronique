import ghostscript

def convert_to_pdfa(input_pdf_path, output_pdfa_path):
	args = [
		"gs",                         # Ghostscript command
		"-dPDFA",                     # Enable PDF/A output
		"-dBATCH",                    # Batch mode: no user interaction
		"-dNOPAUSE",                  # No pause between pages
		"-dNOOUTERSAVE",              # Disable outer save level
		"-sProcessColorModel=DeviceRGB", # Use RGB color model
		"-sDEVICE=pdfwrite",          # Set output device to pdfwrite
		"-dPDFACompatibilityPolicy=1", # PDF/A-1b compliance policy
		f"-sOutputFile={output_pdfa_path}", # Output file path
		input_pdf_path                # Input PDF file
	]

	# Convert arguments into bytes (required by the ghostscript module)
	gs_args = [arg.encode('utf-8') for arg in args]

	# Call Ghostscript with the arguments
	ghostscript.Ghostscript(*gs_args)