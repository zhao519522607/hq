<?php
require __DIR__ . '/vendor/autoload.php';
use AlibabaCloud\Client\AlibabaCloud;
use AlibabaCloud\Client\Exception\ClientException;
use AlibabaCloud\Client\Exception\ServerException;

// Download：https://github.com/aliyun/openapi-sdk-php-client
// Usage：https://github.com/aliyun/openapi-sdk-php-client/blob/master/README-CN.md

AlibabaCloud::accessKeyClient('key', 'rsa')
                        ->regionId('cn-hangzhou') // replace regionId as you need
                        ->asGlobalClient();

function mysql_select() {
	$conn = mysql_connect('mysql-host','usename','password');//连接数据库服务器
	mysql_select_db("db", $conn);
	$result = mysql_query('select ip from crawler_ip where MTIME >= now()-interval 5 HOUR;');
	//$result = mysql_query('select ip from crawler_ip where MTIME >= now()-interval 2 MINUTE;');
	$data = array();
	while ($row = mysql_fetch_row($result)) {
		$data[] = $row;
	}
	return $data;
	mysql_close($conn);
}

function query() {
	try {
		$result = AlibabaCloud::rpcRequest()
                          ->product('dcdn')
                          // ->scheme('https') // https | http
                          ->version('2018-01-15')
                          ->action('DescribeDcdnDomainConfigs')
                          ->method('POST')
                          ->options([
                                        'query' => [
                                          'DomainName' => 'api.aa.com',
                                          'FunctionNames' => 'ip_black_list_set',
                                        ],
                                    ])
                          ->request();
		//print_r($result->toArray());
		return($result->toArray()['DomainConfigs']['DomainConfig'][0]['FunctionArgs']['FunctionArg'][0]['ArgValue']);
	} catch (ClientException $e) {
		echo $e->getErrorMessage() . PHP_EOL;
	} catch (ServerException $e) {
		echo $e->getErrorMessage() . PHP_EOL;
	}
}

function insert($ipblack) {
	try {
		$result = AlibabaCloud::rpcRequest()
                          ->product('dcdn')
                          // ->scheme('https') // https | http
                          ->version('2018-01-15')
                          ->action('BatchSetDcdnDomainConfigs')
                          ->method('POST')
                          ->options([
                                        'query' => [
                                          'DomainNames' => 'api.aa.com',
                                          'Functions' => '[{"functionArgs":[{"argName":"ip_list","argValue":"'.$ipblack.'"}],"functionName":"ip_black_list_set"}]',
                                        ],
                                    ])
                          ->request();
		print_r($result->toArray());
	} catch (ClientException $e) {
		echo $e->getErrorMessage() . PHP_EOL;
	} catch (ServerException $e) {
		echo $e->getErrorMessage() . PHP_EOL;
	}
}

$exis_str = query();
$add_arry = mysql_select();
$add_str = "";
if (count($add_arry)>0) {
	foreach ($add_arry as $value) {
		$add_str = $add_str . $value[0] . ",";
	}
}

if ($add_str != "") {
	$add_str = substr($add_str,0,strlen($add_str)-1);
	$ipblack_str = $exis_str . "," . $add_str;
}
else {
	$ipblack_str = $exis_str;
}

if ($ipblack_str != $exis_str) {	
	$ipblack_list = array_unique(explode(',',$ipblack_str));
	$ipblack_list_count = count($ipblack_list);
	$ipblack_uniq_str = implode(",", $ipblack_list);
	//echo $ipblack_list_count;
	//echo $ipblack_uniq_str;
	insert($ipblack_uniq_str);
}
