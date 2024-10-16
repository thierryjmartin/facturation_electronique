from setuptools import setup, find_packages

setup(
	name='facture_electronique_sdk',
	version='0.1.0',
	author='Thierry Martin',
	author_email='thierry.martin.2008@gadz.org',
	description="Facturation Electronique SDK est une bibliothèque Python qui simplifie l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro**, et d'autres partenaires privés. Elle supporte également le format Factur-X pour la création et l'envoi de factures électroniques.",
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://gitlab.com/cleverip/fr-efact-python-sdk.git',
	packages=find_packages(),
	install_requires=[
		# List of dependencies (from requirements.txt, for example)
	],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.6',  # Specify Python version compatibility
	include_package_data=True,  # If you have extra files to include (via MANIFEST.in)
)