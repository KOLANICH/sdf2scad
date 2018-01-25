include <scad-utils/linalg.scad>

function normalize(vec) = vec / norm(vec);

function identity3()=[[1,0,0],[0,1,0],[0,0,1]];

module rot2Vec(v2, v1=[0, 0, 1]){
	v1=v1;
	v2=normalize(v2);
	
	ax=cross(v1, v2);
	c=v1 * v2;
	ssc = [
		[0, -ax[2], ax[1]],
		[ax[2], 0, -ax[0]],
		[-ax[1], ax[0], 0]
	];
	
	m=identity3() + ssc + (ssc*ssc)*(1-c)/(ax*ax);
	//echo(m);
	multmatrix(m)
		children();
};

module singleBond(l1, l2, color1, color2){
	union(){
		color(color2)
			cylinder(h=l2, r=bondR);
		translate([0, 0, -l1])
			color(color1)
				cylinder(h=l1, r=bondR);
	}
};

module bond(a1v, a2v, color1, color2, multiplicity=1){
	a1v=a1v*lFact;
	a2v=a2v*lFact;
	centr=(a2v+a1v)/2;
	bondVec=normalize(a2v-a1v);
	//echo(bondVec);
	l1=norm(centr-a1v);
	l2=norm(centr-a2v);
	mOfs=multiplicity%2;
	bondSpace=bondSpacingFactor*bondR;
	translate(centr){
		union(){
			rot2Vec(bondVec){
				if (multiplicity>1){
					for (i = [0: multiplicity-1]){
						rotate(360/multiplicity*i, [0,0, 1])
							translate([0, bondSpace, 0])
								singleBond(l1, l2, color1, color2);
					};
				}else{
					singleBond(l1, l2, color1, color2);
				};
			};
		};
	};
};

