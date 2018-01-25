from mol.parser import parse as parseMol
import solid as sld
import mendeleev
import webcolors

from plumbum import cli

class rot2Vec(sld.OpenSCADObject):
	def __init__(self, v2, v1=[0, 0, 1]):
		sld.OpenSCADObject.__init__(self, 'rot2Vec', {"v2":v2, "v1":v1})

def rotByVec(v):
	return rot2Vec(v)

def convertWebColorToOpenScad(cstr):
	try:
		res = webcolors.hex_to_name(cstr)
	except:
		res = [c/255 for c in webcolors.hex_to_rgb(cstr)]
	#res.append(0.5)
	return res

class singleBond(sld.OpenSCADObject):
	def __init__(self, l1, l2, centr, length, color1, color2):
		sld.OpenSCADObject.__init__(self, 'singleBond', {
			"l1":l1,
			"l2":l2,
			"color1": color1,
			"color2": color2,
		})

def makeSingleBond(l1, l2, center, length, color1, color2):
	return singleBond(l1, l2, center, length, convertWebColorToOpenScad(color1), convertWebColorToOpenScad(color2))

class bond(sld.OpenSCADObject):
	def __init__(self, a1v, a2v, color1, color2, multiplicity=1):
		sld.OpenSCADObject.__init__(self, 'bond', {
			"a1v":a1v,
			"a2v":a2v,
			"color1": color1,
			"color2": color2,
			"multiplicity": multiplicity
		})

def makeBond(a1v, a2v, color1, color2, multiplicity=1):
	return bond(a1v, a2v, convertWebColorToOpenScad(color1), convertWebColorToOpenScad(color2), multiplicity=multiplicity)

class module(sld.OpenSCADObject):
	def __init__(self, **kwargs):
		sld.OpenSCADObject.__init__(self, 'module', kwargs)

def useOpenScadVariable(obj, vars={}):
	s=sld.scad_render(obj)
	for placeholder, replacement in vars.items():
		s=s.replace('"'+placeholder+'"', replacement)
	return s

def genScadSource(name, vectors, spieces, bonds, lFact=1, r=1, bondR=None, bondSpacingFactor=3):
	if not bondR:
		bondR=0.05*r
	
	spiecesDescr = {el:mendeleev.element(el) for el in spieces}
	maxRad=max( (sp.covalent_radius for sp in spiecesDescr.values()) )
	
	def createElementCall(name, el):
		class element(sld.OpenSCADObject):
			def __init__(self, pos):
				sld.OpenSCADObject.__init__(self, el.name, {"pos":pos})
		element.__name__=el.name
		return element
	
	
	elToScadRemap={elN:createElementCall(elN, sp) for elN, sp in spiecesDescr.items()}
	
	spiecesChem = [spiecesDescr[el] for el in spieces]
	spiecesScad = [elToScadRemap[el] for el in spieces]

	def createElementModule(name, sp):
		elModSrc="module "+sp.name+"(pos=[0,0,0]){"+useOpenScadVariable(
			sld.translate("%%%positionExprPlaceholder%%%")(
				sld.color(convertWebColorToOpenScad(sp.cpk_color))(
					sld.sphere(r*sp.covalent_radius/maxRad)
				)
			),
			{"%%%positionExprPlaceholder%%%": "pos*lFact"}
		)+"\n}"
		return elModSrc
	
	src=[
		"$fs=0.1;",
		"r="+str(r)+";",
		"bondR="+str(bondR)+";",
		"lFact="+str(lFact)+";",
		"bondSpacingFactor="+str(bondSpacingFactor)+";",
		"include <./util.scad>",
	]
	src.extend((createElementModule(elN, sp) for elN, sp in spiecesDescr.items()))
	
	for i, v in enumerate(vectors):
		src.append(
			sld.scad_render(
				spiecesScad[i](v)
			)
		)
	
	for i, (a1, a2, mult) in enumerate(bonds):
		src.append(
			sld.scad_render(
				makeBond(vectors[a1], vectors[a2], spiecesChem[a1].cpk_color, spiecesChem[a2].cpk_color, mult)
			)
		)
	return src

class mol2scadApp(cli.Application):
	"""Converts .mol and .sdf files into OpenSCAD .scad files, which can be rendered into 3D models."""
	
	r=cli.SwitchAttr(["radius"], float, default=1., help="A radius of the biggest atom.")
	bondRFactor=cli.SwitchAttr(["bond-radius-factor"], float, default=0.05, help="A radius of a single bond is this number multiplied by radius of the largest atom.")
	bondSpacingFactor=cli.SwitchAttr(["bond-spacing-factor"], float, default=3., help="When a bond is multiple its parts are placed on the circumference of the bond radius multiplied by this number.")
	lFact=cli.SwitchAttr(["l-factor"], float, default=1., help="A factor bond length are multiplied. Useful when atoms overlap and you want to see bonds clearly.")
	
	def main(self, fileName:cli.ExistingFile):
		print("\n".join(genScadSource(*parseMol(fileName), lFact=self.lFact, r=self.r, bondR=self.bondRFactor*self.r, bondSpacingFactor=3)))

mol2scadApp.run()
