#!/usr/local/bin/perl --
#!/usr/bin/perl --
# 110326rearng,110311($hta_rest?除去,src変換,他reArng),100421(focus＆ime-mode追加)
# Synopsis  htac.cgi?htapt=dir/file[cgi?yyy]	(dir表記 /ddと../dd は同等、両書式可)
### target-cgi直接アクセス時のid:pwチェックcookie処理 ###↓
# Create passWord: crypt("pwd","MD") => ${it}_htpasswd.txt
($it,$ext)=( $0=~m/([^\/]+)(\..+)$/ );
use CGI "escape","unescape";				# URIencode,decode
$cgi=CGI->new;
$query=unescape($ENV{QUERY_STRING});
($htapt,$hta_rest)=($query=~/htapt=([^\?]*)\?*(.*)$/);	# xx.cgi?yyyをxx.cgiとyyyに分離
							#↑ "?"無ければ$1のみ,$2は空文字
$htapt=~s/^\//\.\.\//;					# /dir/xx -> ../dir/xx
if (-d $htapt){					# inCase(dirのみ indexFile検索→indexFile名付加
	$dir=$htapt;
	for("html","htm","cgi","php","mhl","dat","txt"){
		 if (-f "$htapt/index.$_"){$fexist="$htapt/index.$_"; last;} # index.ext
	}
}
else{
	$fexist=$htapt if (-f $htapt);			# inCase(普通のFile
	$dir=$hta_rest;
}
unless ($fexist) {nofile_exit();}			# file not found

unless ($cgi->cookie($it)) {					# cookie無 id:pwチェック
	$fid=$cgi->param("id");$fpw=$cgi->param("pw");
	pwerr_exit("enter ID PW") unless ($fid && $fpw);
	open F,"cbsc/${it}_htpasswd.txt";			# pswdFile(m0600)
	$str="$fid:".crypt($fpw,"MD");
	(scalar grep{/$str/ } @buf=<F>) ? $cookie="htac=1" : pwerr_exit("ID PW Error<br>");
	close F;			# ↑クッキー(domain,path,expiresオミット)セット
}
### target-cgi直接アクセス時のid:pwチェックcookie処理 ###
# requireで呼ばれるcgi側の処理、$ENV{HTTP_COOKIE}又は$cookieargでクッキーチェック、否の場合、
#  javascript:location.replace("htac.cgi?xx.cgi?yyy")等でhtac.cgiのid:pwチェックに戻す。

if ($htapt=~/\.cgi/) {					#inCase(cgiFile
	$0=$htapt;
	$ENV{QUERY_STRING}=escape($hta_rest);	# URIencoeクエリ再設定、target-cgiに引渡
	$cookiearg=$cookie;			# cookie target-cgiに引渡
	require $htapt; exit;
}
open F,$fexist;						# 存在するfileコンテンツ処理 
read F,$_,1024*1024; close F;				# file読込$_ Max size 1MB
if ( $fexist=~/(html|htm|mhl|dat|txt)$/ || (-T F) ){	# inCase(テキストfile
	s/(<a href=)/$1."$it$ext?htapt=$dir\/"/ieg;	# a_href img src補正
	s/(<img src=)/$1."$it$ext?htapt=$dir\/"/ieg;
	print $cgi->header(-charset=>"",-cookie=>$cookie); print ;
}
else{							# inCase(バイナリその他file
	print $cgi->header("application/octet-stream",-charset=>"",-cookie=>$cookie); print ;
}
#------------------------------------------------------
sub nofile_exit{
 print $cgi->header(-charset=>""),
 "<html>can not open File $pathinfo <a href=javascript:history.back()>GoBack</a>";
exit;								# $ENV{HTTP_REFERER}
}			# DBG ↓$pathinfo未使用 ？？？
			# ${it}${ext}/${pathinfo} => htac.cgi/sc/htac.cgi/sc/cf
			# ${pathinfo} => sc/htac.cgi/sc/cf
#------------------------------------------------------
sub pwerr_exit{
 print $cgi->header(-charset=>""),
 "<html>$_[0]<br><form method=post action=$requesturi>ID:<input type=text name=id style=ime-mode:disabled;>
 PW:<input type=password name=pw style=ime-mode:disabled;><input type=submit value=Go></form>";
 print <<EOF;
<script type=text/javascript><!-- //scriptは＜!--で改行(連続不可)、focus実行前に要form先置
document.forms[0].elements[0].focus();
// --></script></html>
EOF
 exit;
}
#------------------------------------------------------
__END__
************** htac.cgi仕様 *************

xxx.cgi(revise) cookieチェック{ Err enter id:pw <a href=htac.cgi?htapt=xxx.cgi> history.go(-1) }、
print $cgi->header(-charset=>"",-cookie=>$cookie);#(cookie set済)   -> オリジナルで動作
dbu,dbt, ...                                
================
              -------------------------------------------> notfound history.go(-1)
              |
              |                 -------------------------> enter idpw
              |                 |
              |         -------idpw----       -----------> redirect(htapth)
              |         |             |       |
htac.cgi----htapt----cookie-----------+----path600---->>


>>----htapt(/.cgi/)------- $0=htapt; require htapt; --> オリジナルで動作
               |
           |
           ---cat(htapt)--cvrt--|-- <a href=(htac.cgi?htapt=)
                            |
                            |-- <form action=(htac.cgi?htapt=)
                            |
                            |-- <base href=(htac.cgi?htapt=)
--------------------------------------------
