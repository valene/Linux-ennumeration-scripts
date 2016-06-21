#!/usr/bin/perl

use strict;
use warnings;

sub usage{
	print "$0 log file \n" and exit 0;
}

sub regfunc{
	$_[0] =~ m/HEAD/g and print"@_" ;
	$_[0] =~ m/(P|p)ass/g and print"@_" ;
	$_[0] =~ m/(L|l)og/g and print"@_" ;
	$_[0] =~ m/(k|K)ey/g and print"@_" ;
	$_[0] =~ m/private/gi and print"@_" ;
	$_[0] =~ m/rsa/gi and print"@_" ;
	$_[0] =~ m/hash/gi and print"@_" ;
	
}

my $inpfile = $ARGV[0] ;
$inpfile or usage ;
$inpfile and $inpfile eq "-h" and usage ;

open(FH,$inpfile) or die "$!" ; 
while(<FH>) {
	regfunc($_);
}
