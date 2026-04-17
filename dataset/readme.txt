1. obtencion_proteinas.ipnyb
Descarga y filtra secuencias de proteínas desde PDB.  
Elimina redundancia y separa en conjuntos “Similar” y “Novel”.  
Genera los FASTA base (WT) para el resto del flujo.

2. generacion_mut_del.ipnyb
Toma las proteínas WT y genera variantes con mutaciones y deleciones en distintos niveles.
Exporta nuevos FASTA con todas las variantes (WT, mutadas y con deleciones).

3. exp1_mutaciones_deleciones.ipnyb
Compara estructuras de variantes vs WT usando AlphaFold2 y ESMFold.  
Calcula métricas como TM-score y RMSD, analiza estabilidad estructural y confianza (pLDDT).  
Genera tablas y gráficas de resultados.

4. exp2_foldseek.ipnyb
Usa Foldseek para comparar estructuras contra bases de datos.  
Relaciona similitud estructural con pLDDT y analiza correlaciones.

