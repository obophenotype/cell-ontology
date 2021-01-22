#!/usr/bin/perl -w

use strict;

my $show_context;
my %tag_h;
while ($ARGV[0] =~ /^\-.+/) {
    my $opt = shift @ARGV;
    if ($opt eq '-h' || $opt eq '--help') {
        print usage();
        exit 0;
    }
    elsif ($opt eq '-c') {
        $show_context = 1;
    }
    elsif ($opt eq '-l') {
        %tag_h = 
            (
             is_a => 1,
             relationship => 1
            );
    }
    else {
        die $opt;
    }
}

my $f1 = shift @ARGV;
my $f2 = shift @ARGV;

my %ftypeh = ();
my %nh = ();

print STDERR "Parsing: $f1\n";
my $doc1 = pdoc($f1);

print STDERR "Parsing: $f2\n";
my $doc2 = pdoc($f2);

my @ids =  (keys %$doc1,
            keys %$doc2);

@ids = sort @ids;
printf STDERR "Comparing: %d IDs\n", scalar(@ids);
my %doneh = ();
foreach my $id (@ids) {
    next if $doneh{$id};
    $doneh{$id} = 1;
    my @plus = ();
    my @minus = ();
    my @u = ();
    foreach my $v (@{$doc1->{$id}||[]}) {
        if (grep {smatch($v,$_)} @{$doc2->{$id} || []}) {
            push(@u, $v);
        }
        else {
            push(@minus, $v);
        }
    }
    foreach my $v (@{$doc2->{$id}||[]}) {
        if (grep {smatch($v,$_)} @{$doc1->{$id} || []}) {
            
        }
        else {
            push(@plus, $v);
        }
    }
    if (scalar(@plus) || scalar(@minus)) {
        my $chg = '';
        if (!$doc1->{$id}) {
            $chg = '+';
        }
        if (!$doc2->{$id}) {
            $chg = '-';
        }
        my $n = $nh{$id};
        printf "%s[%s]\n",$chg,$ftypeh{$id};
        print $chg."id: $id ! $n\n";
        foreach (@minus) {
            print "-$_\n";
        }
        foreach (@plus) {
            print "+$_\n";
        }
        if ($show_context) {
            foreach (@u) {
                print '#'."$_\n";
            }
        }
        print "\n";
    }
}


exit 0;

sub pdoc {
    my $f = shift;
    my $doc = {};
    my $id;
    my $ftype;
    open(F,$f) || die $f;
    while (<F>) {
        chomp;
        if (/^\[(\S+)\]/) {
            $ftype = $1;
        }
        elsif (/^id:\s*(\S+)/) {
            $id = $1;
            $ftypeh{$id} = $ftype;
            #print STDERR "$id ==> $ftype\n";
        }
        else {
            if (!$id) {
                next;
            }

            if (/^namespace:/) {
                # TODO - make optional
                next;
            }

            if (/^name:\s*(.*)/) {
                my $n = $1;
                if ($nh{$id}) {
                    if ($nh{$id} ne $n) {
                        $nh{$id} .= ' --> ' . $n;
                    }
                }
                else {
                    $nh{$id} = $n;
                }
            }

            if (%tag_h) {
                if (/^(\S+):\s*(.*)/) {
                    if (!$tag_h{$1}) {
                        next;
                    }
                }
            }

            if (/^(\S+):\s*(.*)/) {
                push(@{$doc->{$id}}, $_);
            }
            else {
                $id = '';
            }
        }
    }
    close(F);
    return $doc;
}

sub scriptname {
    my @p = split(/\//,$0);
    pop @p;
}

sub smatch {
    my ($v1,$v2) = @_;
    $v1 = trim($v1);
    $v2 = trim($v2);
    return $v1 eq $v2;
}

sub trim {
    my $x = $_[0];
    $x =~ s/\s*\!.*//;
    $x =~ s/\s+/ /g;
    $x =~ s/^\s+//;
    $x =~ s/\s+$//;
    return $x;

}

sub usage {
    my $sn = scriptname();

    <<EOM;
$sn OBO-FILE1 OBO-FILE2

Compares two obo files



EOM
}

