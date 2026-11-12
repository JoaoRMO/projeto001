# Gera entregas.svg (vetorial) a partir dos dados abaixo.
W,H=1536,1024
rows=[
 ("D1","#0B5FC4","#0B2F63","#DCEAFC",["Projeto","Executivo"],["Documentos aprovados"],
  ["Quantidade de documentos do projeto","com todas as análises e aprovações pelos","órgãos respectivos."]),
 ("D2","#1E8A2E","#1E8A2E","#DFF3E1",["Aquisições"],["Equipamentos entregues"],
  ["Quantidade de equipamentos e materiais","que foram entregues e recebidos no","projeto."]),
 ("D3","#FF8A00","#FF8A00","#FFE8CC",["Construção"],["m² construídos"],
  ["Quantidade de metros quadrados de","área construída, acumulada e aceita","pela fiscalização."]),
 ("D4","#5B2EA6","#5B2EA6","#E6E0F5",["Instalações"],["Metros de tubulação","instalados"],
  ["Quantidade de metros lineares de","tubulação instalada e verificada","conforme projeto."]),
 ("D5","#0E8A94","#0E8A94","#D5F2F1",["Testes"],["Quantidade de testes","realizados"],
  ["Quantidade de testes executados e","aprovados conforme plano de testes","do projeto."]),
]
X0,Y0,OW,OH=18,12,1500,998
HH=70; RT=Y0+HH; RH=(Y0+OH-RT)/5
S='stroke-linecap="round" stroke-linejoin="round" fill="none"'

def check(cx,cy,c,r=24):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" stroke="#fff" stroke-width="4"/>'
            f'<path d="M{cx-r*.45} {cy+r*.02} L{cx-r*.1} {cy+r*.38} L{cx+r*.5} {cy-r*.35}" stroke="#fff" stroke-width="7" {S}/>')

def left_icon(i,c):
    w=f'stroke="{c}" stroke-width="6" {S}'
    if i==0:
        return (f'<path d="M-62 -66 H62 V62 H-62 Z M-62 -66 Q-88 -66 -88 -40 V50 Q-88 66 -72 66 H-30" {w}/>'
                f'<path d="M-52 -52 H52 M-26 8 V-30 H12 V8 M-26 8 H12 M-16 -20 h8 M-16 -8 h8 M0 -20 h8 M0 -8 h8 M-36 28 H20" {w} stroke-width="5"/>'
                f'<path d="M20 52 L48 6 L66 16 L38 62 L14 68 Z" fill="#fff" {w}/>')
    if i==1:
        return (f'<path d="M-92 -52 H-72 L-40 40 H62" {w}/>'
                f'<path d="M-20 -40 L18 -58 L58 -40 V0 L18 18 L-20 0 Z M-20 -40 L18 -22 L58 -40 M18 -22 V18" {w}/>'
                f'<circle cx="-48" cy="60" r="14" {w}/><circle cx="44" cy="58" r="12" {w}/>')
    if i==2:
        return (f'<path d="M-50 -66 V70 M-22 -66 V70 M-50 -66 L-22 -32 L-50 2 L-22 36 L-50 70 M-22 -66 L-50 -32 M-70 70 H0" {w} stroke-width="5"/>'
                f'<path d="M-92 -66 H72 M-36 -66 V-86 M-36 -86 L-86 -66 M-36 -86 L60 -66 M56 -66 V-38 M56 -38 h8" {w} stroke-width="5"/>'
                f'<path d="M30 70 V0 H88 V70 M24 70 H94 M42 14 h8 M58 14 h8 M74 14 h8 M42 30 h8 M58 30 h8 M74 30 h8 M54 70 V50 H68 V70" {w} stroke-width="5"/>')
    if i==3:
        p="M-76 -44 H10 Q44 -44 44 -14 Q44 16 10 16 H-30 Q-64 16 -64 40 Q-64 62 -30 62 H64"
        return (f'<path d="{p}" stroke="{c}" stroke-width="30" fill="none" stroke-linejoin="round"/>'
                f'<path d="{p}" stroke="#fff" stroke-width="18" fill="none" stroke-linejoin="round"/>'
                f'<path d="M-86 -62 V-26 M-62 -62 V-26 M68 46 V78 M92 46 V78" {w}/>'
                f'<path d="M-30 -62 V-26 M18 -62 V-26" {w} stroke-width="5"/>')
    if i==4:
        return (f'<path d="M-90 -50 H-50 M-30 -50 H-10 M-90 -50 V70 H0" {w}/>'
                f'<path d="M-70 -70 H-30 V-50 H-70 Z M-90 -50 H-10 V6" {w} stroke-width="5"/>'
                f'<path d="M-76 -24 l8 8 14 -16 M-76 8 l8 8 14 -16 M-76 40 l8 8 14 -16 M-40 -22 H-14 M-40 10 H-14 M-40 42 H-14" {w} stroke-width="5"/>'
                f'<path d="M30 -10 H78 M42 -10 V26 L12 62 Q8 70 18 70 H90 Q100 70 96 62 L66 26 V-10 M26 40 H84" {w} stroke-width="5"/>'
                f'<circle cx="52" cy="52" r="4" fill="{c}"/><circle cx="72" cy="56" r="3" fill="{c}"/>')

def right_icon(i,c,bg,cx,cy):
    w=f'stroke="{c}" stroke-width="6" {S}'
    g=f'<circle cx="{cx}" cy="{cy}" r="85" fill="{bg}"/><g transform="translate({cx},{cy})">'
    if i==0:
        g+=(f'<path d="M-36 -52 H14 L40 -26 V50 H-36 Z M14 -52 V-26 H40" fill="#fff" {w}/>'
            f'<path d="M-22 -20 H4 M-22 -4 H18 M-22 12 H6" {w} stroke-width="5"/>'+check(34,34,"#1E9E3A"))
    if i==1:
        g+=(f'<path d="M-62 -34 H8 V30 H-62 Z M8 -22 H34 L50 0 V30 H8" {w}/>'
            f'<circle cx="-34" cy="32" r="12" fill="#fff" {w}/><circle cx="28" cy="32" r="12" fill="#fff" {w}/>')
    if i==2:
        g+=(f'<g fill="{c}"><rect x="-62" y="-30" width="30" height="16" rx="2"/><rect x="-62" y="-10" width="22" height="16" rx="2"/>'
            f'<rect x="-36" y="-10" width="22" height="16" rx="2"/><rect x="-62" y="10" width="30" height="16" rx="2"/>'
            f'<rect x="-28" y="10" width="30" height="16" rx="2"/><rect x="6" y="10" width="30" height="16" rx="2"/>'
            f'<rect x="-40" y="30" width="30" height="16" rx="2"/><rect x="-6" y="30" width="30" height="16" rx="2"/></g>'
            f'<path d="M-6 8 L28 -40 L50 -24 L16 18 Z" fill="#fff" {w} stroke-width="5"/><path d="M28 -40 L40 -56 L58 -42 L50 -24" fill="{c}" {w} stroke-width="5"/>')
    if i==3:
        g+=(f'<path d="M-10 -52 H20 Q34 -52 34 -38 V-26 M-10 -52 V-40 M-18 -40 H6 M34 -26 H14 M34 -26 H44 M14 -26 V10 Q14 26 -2 26 H-36 M-62 4 L-44 -4 V36 L-62 28 Z" {w} stroke-width="5.5"/>'
            f'<path d="M-62 4 Q-72 16 -62 28 M-36 12 V36" {w} stroke-width="5.5"/>')
    if i==4:
        g+=(f'<path d="M-44 -34 H-20 M0 -34 H24 M-44 -34 V50 H8 M24 -34 V-8 M-26 -46 H-2 V-34 H-26 Z" fill="#fff" {w} stroke-width="5.5"/>'
            f'<path d="M-34 -10 l6 6 10 -12 M-34 10 l6 6 10 -12 M-34 30 l6 6 10 -12 M-10 -8 H14 M-10 12 H14 M-10 32 H-2" {w} stroke-width="5"/>'
            +check(34,34,"#0E8A94"))
    return g+'</g>'

o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="17cm" height="11.3333cm" viewBox="0 0 {W} {H}" font-family="Inter, Arial, sans-serif">',
 '<defs><clipPath id="c"><rect x="18" y="12" width="1500" height="998" rx="38"/></clipPath></defs>',
 f'<rect width="{W}" height="{H}" fill="#fff"/><g clip-path="url(#c)">',
 f'<rect x="18" y="12" width="1500" height="{HH}" fill="#0B3566"/>',
 '<text x="395" y="60" font-size="34" font-weight="700" fill="#fff" text-anchor="middle">ENTREGA</text>',
 '<text x="1104" y="60" font-size="34" font-weight="700" fill="#fff" text-anchor="middle">UNIDADE DE MEDIÇÃO</text>']
for i,(cod,c,tc,bg,ent,tit,desc) in enumerate(rows):
    top=RT+i*RH; cy=top+RH/2
    o.append(f'<rect x="18" y="{top:.1f}" width="112" height="{RH:.1f}" fill="{c}"/>')
    o.append(f'<text x="74" y="{cy+14:.1f}" font-size="42" font-weight="800" fill="#fff" text-anchor="middle">{cod}</text>')
    o.append(f'<line x1="130" x2="1518" y1="{top:.1f}" y2="{top:.1f}" stroke="#CFD4DA" stroke-width="2"/>')
    o.append(f'<g transform="translate(268,{cy:.1f}) scale(.84)">{left_icon(i,c)}</g>')
    for k,t in enumerate(ent):
        y=cy+(k-(len(ent)-1)/2)*44+13
        o.append(f'<text x="415" y="{y:.1f}" font-size="38" font-weight="700" fill="{tc}">{t}</text>')
    o.append(right_icon(i,c,bg,834,cy))
    lt,ld=36,31; tot=len(tit)*lt+len(desc)*ld+4; y=cy-tot/2+28
    for t in tit:
        o.append(f'<text x="955" y="{y:.1f}" font-size="33" font-weight="700" fill="{c}">{t}</text>'); y+=lt
    y+=-2
    for t in desc:
        o.append(f'<text x="955" y="{y:.1f}" font-size="25" font-weight="400" fill="#222">{t}</text>'); y+=ld
o.append(f'<line x1="702" x2="702" y1="12" y2="1010" stroke="#CFD4DA" stroke-width="2"/></g>')
o.append('<rect x="19" y="13" width="1498" height="996" rx="37" fill="none" stroke="#C5CBD3" stroke-width="3"/></svg>')
open("entregas.svg","w").write("\n".join(o))
