Dbg dbu.cgi  commandLine実行結果不正：  print `cat tmp.txt`;実行正常、print "<pass>1111<b>";
 [ﾚ] escHTML実行(modeSW[X]pipe/IO_selのon/off同じ) → result"<pass>1111<b>" src"print "1111";" これ以降の画面文字太字となる。
  formデータのdwld分、memoとbodyはescHTMLされてる。 modeSW[X]pipe/IO_sel使う？ 一時的 STDO pipeで切替？
  
  escHTML(cmdl)のﾁｪｯｸﾎﾞｯｸｽ初期checkedとすべき。 sub escHTML();は CGI HTML::Entities等のモジュール使え？
RevUp dbm.cgi
  複数ファイル同時選択、保存dir/fileName指定、javascriptのﾛｰｶﾙFileIO HTML5 Blob File API 。
  ファイルをアップロードする JavaScriptプログラミング講座 http://hakuhin.jp/js/upload.html <FORM>要素のみを使った静的なupld HTMLだけ、+JavaScript、HTML5 <input type=file name=input_file multiple>で複数可(IE11 html5で可となっとるが？)、multipart/form-dataでupld。ｻｰﾊﾞ側 perl/php/ruby/python リスト解説、perl CGI upload()メソッド使用。
---------------------------------------------------------------------------------------
dbu.cgi with htac.cgi, and dbt.cgi dbm.cgi 



