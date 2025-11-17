# Arquitectura de la Solución



```
virtualization-io-project/
├── virtualization_benchmark.py
├── analysis_visualization.py
├── results.json
└── README.md
```



---

# Componentes Principales

## 1. VirtualizationBenchmark (`virtualization_benchmark.py`)

**Propósito:** Ejecutar benchmarks comparativos reales.

**Funciones clave:**
- `create_disk_image()`: Crea imágenes de disco QCOW2.
- `build_qemu_command()`: Construye comandos QEMU con diferentes backends.
- `simulate_vm_boot()`: Mide tiempos de arranque y métricas de E/S.
- `monitor_cpu_usage()`: Monitorea el uso de CPU del host.
- `run_comparison()`: Ejecuta la suite completa de comparación.

---

## 2. VirtualizationAnalyzer (`analysis_visualization.py`)

**Propósito:** Análisis estadístico y generación de visualizaciones.

**Funciones clave:**
- `load_results()`: Carga resultados desde JSON.
- `create_comparison_charts()`: Genera gráficos comparativos.
- `generate_detailed_report()`: Produce análisis textual detallado.

---

# Requisitos del Sistema

## Software Requerido
- Python 3.8+
- QEMU 4.0+ (opcional)
- Linux (Ubuntu 20.04+ recomendado)

## Librerías Python
- `psutil >= 5.9.0`
- `matplotlib >= 3.5.0`
- `numpy >= 1.21.0`

---

# Guía de Ejecución

## Crear entorno virtual

- `python3 -m venv venv`
- `source venv/bin/activate`

En Windows:

- `venv\Scripts\activate`

Instalar dependencias

 - `pip install --upgrade pip`
 - `pip install psutil numpy matplotlib` 

Verificar instalación

- `python3 -c "import psutil, numpy, matplotlib; print('✓ Todas las dependencias instaladas correctamente')"`

Ejecución del Proyecto
1. Ejecutar benchmarks

- `python3 virtualization_benchmark.py`

Resultado: Se genera results.json con las métricas.

2. Generar análisis y visualizaciones
- `python3 analysis_visualization.py`

## Archivos de Salida
- results.json

- virtualization_comparison.png

- detailed_analysis.txt

## Manejo de Excepciones
Errores comunes
- FileNotFoundError: QEMU no instalado
Solución: Instalar QEMU o usar modo simulación.

- PermissionError: Permisos insuficientes
Solución: Ejecutar con privilegios adecuados o sin --real-vm.

-  MemoryError: Recursos insuficientes
Solución: Reducir --memory y --disk-size.

## Códigos de Error
```
Código	   | Significado
0	       | Ejecución exitosa
1	       | Error general
2	       | Argumentos inválidos
3	       | Recursos insuficientes
```
# SO_Input_Output_Virtualization
# SO_Input_Output_Virtualization_Sustentacion
