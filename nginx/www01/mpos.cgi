#!/usr/bin/perl
$attach_dir  = "/home/sarirasa/htdocs/tmp/";
require "date.pl";
require "cgi-lib.pl";

use CGI;
use DBI;

&ReadParse(*in);

use POSIX;
$datefile = POSIX::strftime(
             "%d%m%y %H%M%S",
             localtime(
                 ( stat $filepages )[9]
                 )
             );

print "Content-type: text/html\n";
print "Cache-Control: no-store\n";
$dbp = DBI->connect("dbi:Firebird:db=/home/sarirasa/data/sispos.fdb;ib_dialect=3", "SISPOS", "masterpos") or die $DBI::errstr;

  @numbers = split(/\./, $ENV{REMOTE_ADDR});
  $ip_number = pack("C4", @numbers);
  #$hostname = (gethostbyaddr($ip_number, 2))[0];
  $agent=uc($ENV{HTTP_USER_AGENT});
  if ((index($agent,'MOBILE') != -1) || (index($agent,'ANDROID') != -1))
  {
    $mobil='Y';
  } else {
    $mobil='N';
  }
  $filepages='/home/sarirasa/cgi-bin/mpage/'.$in{pages}.'.pl';

@tmp_tgl=split(/\s+/,localtime);
$tmp_tgl[2]=~s/^([1-9])$/0$1/;
if (length($tmp_tgl[2])<2) {
$tmp_tgl[2]='0'.$tmp_tgl[2];
}

%tmp_bln=(Jan,"01",Feb,"02",Mar,"03",Apr,"04",May,"05",Jun,"06",Jul,"07",Aug,"08",Sep,"09",Oct,"10",Nov,"11",Dec,"12");
%tmp_rom=(Jan,"I",Feb,"II",Mar,"III",Apr,"IV",May,"V",Jun,"VI",Jul,"VII",Aug,"VIII",Sep,"IX",Oct,"X",Nov,"XI",Dec,"XII");
$tt="$tmp_bln{$tmp_tgl[1]}/$tmp_tgl[2]/$tmp_tgl[4]";
$thntgl="$tmp_tgl[4]$tmp_bln{$tmp_tgl[1]}$tmp_tgl[2]";

$bcolitem="CCFF99";
$bcolnote="CCFFCC";
$bcolnum="CCCCFF";
$bcolsum="FFFFCC";
$menucolor="#FFFFFF";
$header="#800000";
$divheader="#CCCCCC";
$footer="#333333";
$datacolor="#FFFFFF";
$colcolor="#34495F";

opendir(DIRtmp,"tmp");
@FILEtmp=grep(!/^\.\.?$/,readdir(DIRtmp));
closedir(DIRtmp);
#foreach (@FILEtmp){unlink("tmp/$_")if(-M "tmp/$_">0.15);};
$in{nama}=uc($in{nama});
if ($in{panjx}) {
  $panjx=$in{panjx};
  $panjy=$in{panjy};
} else {
  $in{panjx}=$panjx;
  $in{panjy}=$panjy;
}
if ($in{ss})
{
 if ($in{pages})
 {
    open(FILEtmp,"/tmp/$in{ss}");
    $ssss=<FILEtmp>;
    @s3s = split(/\|/,$ssss);
    close(FILEtmp);
    if (($in{pageid}) && ($s3s[6] eq $in{pageid})) {
     $s3s[7]++;} else {
     $s3s[7]=0;
    }
    open(FILEtmp,">/tmp/$in{ss}");   
    print FILEtmp "$s3s[0]|$s3s[1]|$s3s[2]|$s3s[3]|$s3s[4]|$s3s[5]|$in{pageid}|$s3s[7]|$s3s[8]|$s3s[9]|$s3s[10]|$s3s[11]|$s3s[12]|$s3s[13]|$mobil|";
    close(FILEtmp);
    if ($s3s[0] eq "") {
     $ketemu=0;
    }
    else{
     $ketemu=1;
    }
 }
 if ($ketemu)
 {
  $bag_a = "$in{pages}";
 }
 else
 {
  $bag_a = "mpos001";
 }
}
else
{
 $bag_a = "mpos001";
 $psnmuka = "Unvalid Login. Please Try Again." if ($in{nama} || $in{npass});
 opendir(DIRtmp,"tmp");
 @FILEtmp = grep(!/^\.\.?$/,readdir(DIRtmp));
 closedir(DIRtmp);
 #foreach (@FILEtmp) { unlink("tmp/$_") if (-M "tmp/$_" > 0.05); }
 srand($$|time);
 $ss = unpack("H*", pack("Nnn", time, $$, int(rand(99999)))) . ".ss";
 $sth_log = $dbp->prepare("SELECT namauser,npassword,nlengkap,posisi,b.kodestore cabang, b.jns_rest jns_resto, scr, kodeuser,nik
 FROM x0000005 a inner join m_info b on (1=1) where b.isaktif='Y' and a.namauser=?");
 $sth_log->execute($in{nama});
 while( @row = $sth_log->fetchrow_array())
 {

  $row[0] =~ s/ *$// ;
  $row[1] =~ s/ *$// ;
  $row[2] =~ s/ *$// ;
  $row[3] =~ s/ *$// ;
  $row[4] =~ s/ *$// ;
  $row[7] =~ s/ *$// ;
  $row[8] =~ s/ *$// ;
  if ($in{nama} eq $row[0])
  {
   if ($in{npass} eq $row[1])
   {
    $ketemupass = "OK";
    $posuser=$row[3];
    if ($in{npass} eq 'sate') {
      $bag_a="mpos001";
    } else {
      $bag_a="mpos002";
    }
    $s3s[0]=$in{nama};
    $s3s[2]=$row[2];
    $s3s[3]=$row[3];
    $s3s[4]=$row[4];
    $s3s[5]=$row[5];
    $s3s[8]=$row[6];
    $s3s[9]=$row[7];
    $s3s[10]=$row[8];
    $s3s[12]=$in{panjx};
    $s3s[13]=$in{panjy};
    $in{ss}=$ss;
    open(FILEtmp,">/tmp/$ss");    
    print FILEtmp "$in{nama}|$in{npass}|$row[2]|$row[3]|$row[4]|$row[5]||0|$row[6]|$row[7]|$row[8]||$in{panjx}|$in{panjy}|$mobil|";
    close(FILEtmp);
   }
  }
 }
}

require "mpage/$bag_a.pl";

&cetak_halaman;
$dbp->disconnect;
exit;

sub kirim_mail
{
 $prg_mail = "/usr/sbin/sendmail -t";
 open(MAIL,"|$prg_mail");
 print MAIL <<__ENDMAIL__;
To: $mail_kepada
From: $mail_dari
Subject: $mail_subject
$mail_pesan
__ENDMAIL__
 close(MAIL);
}

sub skkkkdd
{
 ($aa1)=@_;
 if ($aa1<0) {
   $sg='-';
 } else {
   $sg='';
 }
 $aa=int(abs($aa1));
 $dd=$aa1-$aa;
 $cc="";
 $bb=length($aa);
 while($bb>3)
 {
  $cc=",".substr($aa,($bb-3),3).$cc;
  $aa=substr($aa,0,($bb-3));
  $bb=length($aa);
 }
 if ($dd >=0.01 ) {
  $dd=int($dd*100);
  if ($dd<10) {
    $dd='0'.$dd;
  }
  $cc=$sg.$aa.$cc.'.'.$dd;
 } else {
  $cc=$sg.$aa.$cc;
 }
}

sub cetak_halaman
{
print qq~
<!doctype html>
<html>
<head>
<title>Sari Rasa Grup - Sate Khas Senayan, Tesate, Call Aja</title>
<link rel="SHORTCUT ICON" href="http://www.sarirasagrup.com/images/sate.ico" />

<style type="text/css">

	/* common page styles */
body {
	font-family: Verdana, Geneva, sans-serif;
	font-size: 18px;
       }

.menu1 {
	font-family: Verdana, Geneva, sans-serif;
	font-size:22px;
	color: #FFF;
}
.menu2 {
	font-family: Verdana, Geneva, sans-serif;
	font-size:22px;
	color: #800000;
}
.huruf0 {
	font-family:Verdana, Geneva, sans-serif;
	font-size:16px;
	color:#000000;
}
.huruf1 {
	font-family:Verdana, Geneva, sans-serif;
	font-size:18px;
	color:#000000;
}

.huruf2 {
	font-family:Verdana, Geneva, sans-serif;
	font-size:18px;
	color:#000000;
  white-space: normal;
}
.huruf3 {
	font-family:Verdana, Geneva, sans-serif;
	font-size:38px;
	color:#000000;
}

.hurufcol {
	font-family:Verdana, Geneva, sans-serif;
	font-size:20px;
	color:#FFFFFF;
}
.huruf10w {
	font-family: Verdana, Geneva, sans-serif;
	font-size:10px;
        color:#FFFFFF;
}
.huruf10b {
	font-family: Verdana, Geneva, sans-serif;
	font-size:10px;
        color:#000000;
}
.smallb {
	font-family: Tahoma, Geneva, sans-serif;
	font-size:10px;
        color:#000000;
}
.smallw {
	font-family: Tahoma, Geneva, sans-serif;
	font-size:10px;
        color:#FFFFFF;
}
.psnclass {
	font-family:Verdana, Geneva, sans-serif;
	font-size:22px;
	color:yellow;
}
.errpsnclass {
	font-family:Verdana, Geneva, sans-serif;
	font-size:22px;
	color:red;
}

.ft0{font-style:normal;font-weight:normal;font-size:11px;font-family:Times-Roman;color:#000000;}
.ft1{font-style:normal;font-weight:bold;font-size:15px;font-family:Times;color:#000000;}
.ft2{font-style:italic;font-weight:normal;font-size:9px;font-family:Times;color:#000000;}
.ft3{font-style:normal;font-weight:bold;font-size:18px;font-family:Helvetica;color:#000000;}
.ft4{font-style:normal;font-weight:bold;font-size:10px;font-family:Helvetica;color:#000000;}
.ft5{font-style:normal;font-weight:normal;font-size:10px;font-family:Helvetica;color:#000000;}

.linklight A:link {text-decoration: none; color:navy}
.linklight A:visited {text-decoration: none; color:blue}
.linklight A:active {text-decoration: none; color:black}
.linklight A:hover {text-decoration: none; color: red;}

.linkdark A:link {text-decoration: none;color:white}
.linkdark A:visited {text-decoration: none; color:yellow}
.linkdark A:active {text-decoration: none; color:white}
.linkdark A:hover {text-decoration: none; color: aqua;}

.td1 {background:#EEEEEE;color:#000;border:1px solid #000;}
.th{background:blue;color:white;border:1px solid #000;}

.div_freezepanes_wrapper{
position:relative;width:90%;height:400px;
overflow:hidden;background:#fff;border-style: ridge;
}

.div_verticalscroll{
position: absolute;right:0px;width:18px;height:100%;
background:#EAEAEA;border:1px solid #C0C0C0;
}

.buttonUp{
width:20px;position: absolute;top:2px;
}

.buttonDn{
width:20px;position: absolute;bottom:22px;
}

.div_horizontalscroll{
position: absolute;bottom:0px;width:100%;height:18px;
background:#EAEAEA;border:1px solid #C0C0C0;
}

.buttonRight{
width:20px;position: absolute;left:0px;padding-top:2px;
}

.buttonLeft{
width:20px;position: absolute;right:22px;padding-top:2px;
}

</style>

<style type="text/css">
/* menu styles */

#jsddm
{	margin: 0;
	padding: 0}

	#jsddm li
	{	float: left;
		list-style: none;
		font: 12px Tahoma, Arial}

	#jsddm li a
	{	display: block;
		background: #FFFFFF;
		padding: 5px 12px;
		text-decoration: none;
		border-right: 1px solid #4F6F8E;
		width: 70px;
		color: #000;
		white-space: nowrap}

	#jsddm li a:hover
	{	background: #000000;
                color: #FFFFFF}

		#jsddm li ul
		{	margin: 0;
			padding: 0;
			position: absolute;
			visibility: hidden;
			border-top: 1px solid white}

			#jsddm li ul li
			{	float: none;
				display: inline}

			#jsddm li ul li a
			{	width: auto;
				background: #E5E5E5;

                border-top: 1px solid #FFFFFF;
				color: #24313C}

			#jsddm li ul li a:hover
			{	background: #FF9;
                                color: #000000}
</style>

<style type="text/css">
#mytable-div table {
border-collapse: collapse;
}
#mytable-div td,th {
border: 1px solid #B3B3B3;
white-space: nowrap;
padding: 2px 4px;
}
</style>

<script language="JavaScript">
function ModifyEnterKeyPressAsTab() {
    if (window.event && window.event.keyCode == 13) {
       window.event.keyCode = 9;
    }
}
</script>

</head>~;
if ($bag_a ne "mpos001") {
print qq~<body>~;
} else {
print qq~<body>~;
}
print qq~
<script src="/jquery.min.js" type="text/javascript"></script>
<script type="text/javascript">
var timeout         = 500;
var closetimer		= 0;
var ddmenuitem      = 0;

function jsddm_open()
{	jsddm_canceltimer();
	jsddm_close();
	ddmenuitem = \$(this).find('ul').eq(0).css('visibility', 'visible');}

function jsddm_close()
{	if(ddmenuitem) ddmenuitem.css('visibility', 'hidden');}

function jsddm_timer()
{	closetimer = window.setTimeout(jsddm_close, timeout);}

function jsddm_canceltimer()
{	if(closetimer)
	{	window.clearTimeout(closetimer);
closetimer = null;}}
\$(document).ready(function()
{\$('#jsddm > li').bind('mouseover', jsddm_open);
\$('#jsddm > li').bind('mouseout',  jsddm_timer);});

document.onclick = jsddm_close;
</script>
~;
 &$bag_a;
print qq~

</body>
</html>
~;
}

