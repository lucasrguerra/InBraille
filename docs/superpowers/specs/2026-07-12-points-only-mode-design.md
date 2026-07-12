# Modo "Apenas os pontos" (sem placa) — Design

Data: 2026-07-12

## Objetivo

Permitir que o usuário gere um STL contendo **apenas as calotas dos pontos Braille**,
sem a placa de base. A intenção é que essas calotas possam ser coladas/integradas em
STLs já existentes (produtos, etiquetas, etc.).

Hoje cada ponto é uma esfera de raio 1mm cujo centro fica em `z = plate_thickness - 0.35`,
de modo que apenas 0.65mm da esfera aparece acima da placa (a "espessura aparente"), e a
placa esconde os 0.35mm inferiores. No modo novo não há placa, então é preciso **cortar a
esfera** no mesmo plano e **fechar o corte** para produzir um sólido watertight.

## Decisões (confirmadas com o usuário)

1. **Geometria do ponto:** calota de exatamente 0.65mm com base plana em `z = 0`.
2. **Barra de orientação:** barra fina ao longo da base inferior, **separada** dos pontos
   (com um pequeno espaço), mesma altura das calotas (0.65mm), coplanar com as bases.
3. **Interface:** checkbox "Apenas os pontos (sem placa)" nas Opções Avançadas que
   **desabilita** as opções que não se aplicam (Placas Separadas, Bordas Arredondadas,
   Espessura da Placa). Alinhamento, Símbolos por Linha e Resolução seguem ativos.

## Geometria da calota

Para uma esfera de raio `r = 1` centrada na origem:
- Topo em `z = r = 1`.
- Cortar no plano `z = r - apparent_thickness = 1 - 0.65 = 0.35`, mantendo a parte superior.
- A calota resultante tem altura `apparent_thickness = 0.65mm` e raio de base
  `sqrt(r^2 - 0.35^2) ≈ 0.937mm`.
- Transladar para baixo em `0.35` para a base ficar em `z = 0`.

Usar `vtkClipClosedSurface` com um `vtkPlaneCollection` (plano com normal +Z e origem em
`z = 0.35`). Esse filtro corta e **fecha a superfície** de corte, garantindo um sólido
manifold/watertight adequado para STL — diferente de `vtkClipPolyData`, que deixa o corte
aberto.

## Componentes

### stl.py

Nova função:

```python
def createBrailleCap(radius=1, apparent_thickness=0.65, resolution=20):
    # cria esfera centrada na origem
    # clipa em z = radius - apparent_thickness com vtkClipClosedSurface (fecha o corte)
    # translada para base em z = 0
    # retorna vtkPolyData (sólido fechado)
```

`createBraillePoints` ganha parâmetro `points_only=False`. Quando `True`, cada ponto usa
`createBrailleCap(...)` (base em `z=0`) no lugar de `createSphere(...)`. Quando `False`,
comportamento inalterado.

Nova função utilitária para a barra:

```python
def createBar(width, depth, height):
    # retângulo (vtkCubeSource) de dimensões dadas, centrado; base em z=0 após translação
```
(pode reutilizar `createPlate` + translação; não precisa de função nova se `createPlate`
servir.)

### braille.py

`characterTo3d` ganha `points_only=False` e o repassa a `createBraillePoints`.

`toSTL` ganha parâmetro `points_only=False`. Quando `True`:
- Ignora criação de placa/bordas (nada de `createPlate`/`createCylinder`/`rounded`).
- Força layout único (`unique_plate` interno = True) para posicionar as linhas.
- `letter_position_z = 0` (base das calotas em z=0). `plate_thickness` é ignorado.
- Passa `points_only=True` a `characterTo3d`.
- Após montar todas as calotas, calcula o bounding box da cena
  (`scene.GetOutput().GetBounds()` → xmin,xmax,ymin,ymax) e adiciona a barra de
  orientação: largura = (xmax - xmin), profundidade em Y ≈ 1.2mm, altura 0.65mm, base em
  z=0, posicionada com um pequeno espaço (`gap ≈ 0.8mm`) abaixo de `ymin`, centralizada em
  X entre xmin e xmax.
- A rotação final de 90° em X (já existente) é mantida, então a barra e as calotas ficam
  na mesma orientação de impressão.

Quando `points_only=False`, o fluxo atual permanece idêntico.

### requests.py

`ToSTLRequest` ganha `points_only: bool | None = None`.

### main.py

`to_stl` lê `points_only = request.points_only if request.points_only else False` e repassa
para `braille.toSTL(...)`.

### Interface (templates + index.js)

- Novo card nas Opções Avançadas (em `index_pt_br.html` e `index_en.html`) com checkbox
  `input_points_only` e texto descritivo.
- `index.js`:
  - Nova variável `points_only` (default `false`) e binding `input_points_only`.
  - `updateParameters` lê o checkbox.
  - `generateSTL` inclui `points_only` no payload.
  - Nova função `applyPointsOnlyState()` que, quando marcado, desabilita e esmaece os
    campos: separate plates, rounded, plate thickness; e reabilita quando desmarcado.
    Chamada no listener do checkbox e no `DOMContentLoaded`.

## Fluxo de dados

Usuário marca checkbox → `points_only=true` no payload POST `/api/to-stl` → `main.py`
repassa a `braille.toSTL(..., points_only=True)` → cena só com calotas + barra → STL.

## Tratamento de erros

- Sem novos caminhos de erro. Se a cena ficar vazia (só espaços), o bounding box é
  inválido; nesse caso não adiciona a barra (guarda contra bounds degenerados).

## Testes / verificação

- Gerar STL em modo normal (regressão: byte-idêntico ao anterior para mesmos parâmetros).
- Gerar STL points-only para uma frase curta e verificar: (a) sem placa; (b) calotas com
  ~0.65mm de altura; (c) barra presente abaixo dos pontos; (d) sólido watertight (inspeção
  no visualizador / contagem de componentes).
- Verificar UI: checkbox desabilita os campos corretos e o payload muda.
