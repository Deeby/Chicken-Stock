import pandas as pd
import pandas_datareader as pdr

# ���� Ÿ�Կ� ���� download url�� �ٸ�. �����ڵ� �ڿ� .KS .KQ���� �ԷµǾ���ؼ� Download Link ���� �ʿ�
stock_type = {
	'kospi': 'stockMkt',
	'kosdaq': 'kosdaqMkt'
}

# ȸ������� �ֽ� ���� �ڵ带 ȹ���� �� �ֵ��� �ϴ� �Լ�
def get_code(df, name):
	code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
	# ���Ͱ��� code���� �������� �տ� ������ �پ��ִ� ��Ȳ�� �߻��Ͽ� �յڷ� sript() �Ͽ� ���� ����
	code = code.strip()
	return code

# download url ����
def get_download_stock(market_type=None):
	market_type = stock_type[market_type]
	download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
	download_link = download_link + '?method=download'
	download_link = download_link + '&marketType=' + market_type
	df = pd.read_html(download_link, header=0)[0]
	return df;

# kospi �����ڵ� ��� �ٿ�ε�
def get_download_kospi():
	df = get_download_stock('kospi')
	df.�����ڵ� = df.�����ڵ�.map('{:06d}.KS'.format)
	return df

# kosdaq �����ڵ� ��� �ٿ�ε�
def get_download_kosdaq():
	df = get_download_stock('kosdaq')
	df.�����ڵ� = df.�����ڵ�.map('{:06d}.KQ'.format)
	return df

# kospi, kosdaq �����ڵ� ���� �ٿ�ε�
kospi_df = get_download_kospi()
kosdaq_df = get_download_kosdaq()

# data frame merge
code_df = pd.concat([kospi_df, kosdaq_df])

# data frame����
code_df = code_df[['ȸ���', '�����ڵ�']]

# data frame title ���� 'ȸ���' = name, �����ڵ� = 'code'
code_df = code_df.rename(columns={'ȸ���': 'name', '�����ڵ�': 'code'})

# �Ｚ������ �����ڵ� ȹ��. data frame���� �̹� XXXXXX.KX ���·� ������ �Ǿ�����
code = get_code(code_df, '�Ｚ����')

# get_data_yahoo API�� ���ؼ� yahho finance�� �ֽ� ���� �����͸� �����´�.
df = pdr.get_data_yahoo(code)