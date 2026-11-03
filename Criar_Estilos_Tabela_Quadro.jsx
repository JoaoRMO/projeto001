// Criar_Estilos_Tabela_Quadro.jsx
// Cria amostras, estilos de célula e estilos de tabela "Tabela" e "Quadro".
// Uso: InDesign > Janela > Utilitários > Scripts > clique direito na pasta "Usuário" > Revelar > cole este arquivo.
//      Depois dê duplo clique no script (com um documento aberto).

// ===== AJUSTE AQUI AS CORES (CMYK 0-100) =====
var AZUL_BASE      = [100, 60, 0, 0];   // azul do traçado
var COR_CABECALHO  = [100, 60, 0, 30];  // cor específica do cabeçalho
var TOM_TRACADO    = 15;                // % do azul no traçado
var TOM_CINZA      = 15;                // % do preto nas linhas alternadas
var PESO_TRACADO   = 0.5;               // pt
// ==============================================

if (app.documents.length === 0) {
    alert("Abra um documento antes de rodar o script.");
} else {
    main(app.activeDocument);
}

function tentar(obj, props, log) {
    for (var k in props) {
        try { obj[k] = props[k]; }
        catch (e) { log.push(obj.name + " -> " + k + ": " + e.message); }
    }
}

function obterOuCriar(col, nome, props) {
    var item = col.itemByName(nome);
    if (!item.isValid) { item = col.add(props || {}); try { item.name = nome; } catch (e) {} }
    return item;
}

// Matizes têm nome somente leitura: procura um existente (mesma cor base e tom) ou cria.
function obterTint(doc, base, valor) {
    for (var i = 0; i < doc.tints.length; i++) {
        var t = doc.tints[i];
        try {
            if (t.baseColor.id === base.id && t.tintValue === valor) return t;
        } catch (e) {}
    }
    return doc.tints.add({ baseColor: base, tintValue: valor });
}

function main(doc) {
    var log = [];

    // --- Amostras ---
    var azul = obterOuCriar(doc.colors, "Azul", null);
    tentar(azul, { model: ColorModel.PROCESS, space: ColorSpace.CMYK, colorValue: AZUL_BASE }, log);

    var cab = obterOuCriar(doc.colors, "Cabeçalho", null);
    tentar(cab, { model: ColorModel.PROCESS, space: ColorSpace.CMYK, colorValue: COR_CABECALHO }, log);

    var azul15 = obterTint(doc, azul, TOM_TRACADO);

    var preto = doc.swatches.itemByName("Black");
    var cinza15 = obterTint(doc, preto, TOM_CINZA);

    var papel = doc.swatches.itemByName("Paper");
    var nenhum = doc.swatches.itemByName("None");

    // --- Estilos de célula ---
    function estiloCelula(nome, fill, horizontais) {
        var cs = obterOuCriar(doc.cellStyles, nome, null);
        var p = {
            fillColor: fill,
            leftEdgeStrokeWeight: 0,
            rightEdgeStrokeWeight: 0,
            topEdgeStrokeWeight: horizontais ? PESO_TRACADO : 0,
            bottomEdgeStrokeWeight: horizontais ? PESO_TRACADO : 0
        };
        if (horizontais) {
            p.topEdgeStrokeColor = azul15;
            p.bottomEdgeStrokeColor = azul15;
        }
        tentar(cs, p, log);
        return cs;
    }

    var csCab = estiloCelula("Cabeçalho", cab, true);
    var csCorpo = estiloCelula("Corpo", papel, true);          // fundo vem da alternância da tabela
    var csCorpoQuadro = estiloCelula("Corpo Quadro", papel, true); // sempre branco

    // --- Estilos de tabela ---
    function estiloTabela(nome, cellBody, alternar) {
        var ts = obterOuCriar(doc.tableStyles, nome, null);
        var p = {
            headerRegionCellStyle: csCab,
            bodyRegionCellStyle: cellBody,
            topBorderStrokeWeight: 0,
            bottomBorderStrokeWeight: 0,
            leftBorderStrokeWeight: 0,
            rightBorderStrokeWeight: 0,
            startColumnStrokeWeight: 0,
            endColumnStrokeWeight: 0
        };
        if (alternar) {
            p.alternatingFills = AlternatingFillsTypes.ALTERNATING_ROWS;
            p.startRowFillColor = papel;
            p.startRowFillCount = 1;
            p.endRowFillColor = cinza15;
            p.endRowFillCount = 1;
            p.skipFirstAlternatingFillRows = 1;
        } else {
            p.alternatingFills = AlternatingFillsTypes.NO_ALTERNATION;
        }
        tentar(ts, p, log);
        return ts;
    }

    estiloTabela("Tabela", csCorpo, true);
    estiloTabela("Quadro", csCorpoQuadro, false);

    if (log.length) {
        alert("Estilos criados, mas algumas propriedades não foram aplicadas:\n\n" + log.join("\n") +
              "\n\nAjuste manualmente em Estilos de tabela.");
    } else {
        alert("Pronto! Criados: estilos de tabela 'Tabela' e 'Quadro' e estilos de célula.");
    }
}
