var x ;
var y ;
var z ;
var w ;
var r ;
if(true)
{
 x  =  4 ;
 y  =  5 ;
 z  =  10 ;
 if  (  z  ===  10  ) {
advance (  z  ) ;
}
 while  (  x + 2 * 3  !==  (  y + 10  )  ) {
turn (  45  ) ;
advance (  x * 10 + z * z  ) ;
 x  =  x + 1 ;
 while  (  x  ===  3  ) {
turn (  45  ) ;
}
}
 w  =  3 ;
 r  =  4 ;
 if  (  w  !==  3  ||  r  ===  3  ) {
turn (  135  ) ;
color (  x * 3  ,  (  y - 1  ) * 100  ,  z * 3  ) ;
}
}
function advance(e){console.log("advance",e);}
function turn(e){console.log("turn",e);}
function color(a,b,c){console.log("color",a,b,c);}
