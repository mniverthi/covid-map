#!/usr/bin/perl
# news2csv.pl
# Google News Results exported to CSV suitable for import into Excel.
# Usage: perl news2csv.pl < news.html > news.csv
     
print qq{"title","link","source","date or age", "description"\n};
     
my %unescape = ('&lt;'=>'<', '&gt;'=>'>', '&amp;'=>'&', 
  '&quot;'=>'"', '&nbsp;'=>' '); 
my $unescape_re = join '|' => keys %unescape;

my $results = join '', <>;
$results =~ s/($unescape_re)/$unescape{$1}/migs; # unescape HTML
$results =~ s![\n\r]! !migs; # drop spurious newlines

while ( $results =~ m!<a href="([^"]+)" id="?r-[0-9]+"?>(.+?)</a>
<br>(.+?)<nobr>(.+?)</nobr>.*?<br>.+?)<br>migs  {
  my($url, $title, $source, $date_age, $description) = 
  ($1||'',$2||'',$3||'',$4||'', $5||'');
  $title =~ s!"!""!g; # double escape " marks
  $description =~ s!"!""!g;
  my $output =
    qq{"$title","$url","$source","$date_age","$description"\n};
  $output =~ s!<.+?>!!g; # drop all HTML tags
  print $output;
}      