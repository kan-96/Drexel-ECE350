

load Add4.hdl,
output-file Add4.out,
compare-to Add4.cmp,
output-list a%B1.4.1 b%B1.4.1 sum%B1.4.1 carry%B3.1.3;

set a %B0000,
set b %B0000,
eval,
output;

set a %B0000,
set b %B1111,
eval,
output;

set a %B1111,
set b %B1111,
eval,
output;

set a %B1010,
set b %B0101,
eval,
output;

set a %B0011,
set b %B1100,
eval,
output;

set a %B0100,
set b %B0110,
eval,
output;
