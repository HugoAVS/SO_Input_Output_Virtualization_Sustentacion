import json
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List
import sys

class VirtualizationAnalyzer:
    def __init__(self, results_file: str = "results.json"):
        self.results_file = results_file
        self.data = None
        self.load_results()
    
    def load_results(self):
        try:
            with open(self.results_file, 'r') as f:
                self.data = json.load(f)
            print(f"[OK] Resultados cargados desde {self.results_file}")
        except FileNotFoundError:
            print(f"[ERROR] Archivo {self.results_file} no encontrado")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"[ERROR] Formato JSON inválido en {self.results_file}")
            sys.exit(1)
    
    def create_comparison_charts(self):
        if not self.data or 'metrics' not in self.data:
            print("[ERROR] Datos no disponibles para visualización")
            return
        
        metrics = self.data['metrics']
        if len(metrics) < 2:
            print("[ERROR] Se necesitan al menos 2 conjuntos de métricas")
            return
        
        virtio = metrics[0]
        emulated = metrics[1]
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Comparación Virtio vs Dispositivos Emulados', 
                     fontsize=16, fontweight='bold')
        ax1 = axes[0, 0]
        categories = ['Virtio', 'Emulado']
        boot_times = [virtio['boot_time'], emulated['boot_time']]
        bars1 = ax1.bar(categories, boot_times, color=['#2ecc71', '#e74c3c'])
        ax1.set_ylabel('Segundos')
        ax1.set_title('Tiempo de Arranque')
        ax1.grid(axis='y', alpha=0.3)
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}s',
                    ha='center', va='bottom')
        ax2 = axes[0, 1]
        read_speeds = [virtio['disk_read_speed'], emulated['disk_read_speed']]
        bars2 = ax2.bar(categories, read_speeds, color=['#2ecc71', '#e74c3c'])
        ax2.set_ylabel('MB/s')
        ax2.set_title('Velocidad de Lectura de Disco')
        ax2.grid(axis='y', alpha=0.3)
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

        ax3 = axes[0, 2]
        write_speeds = [virtio['disk_write_speed'], emulated['disk_write_speed']]
        bars3 = ax3.bar(categories, write_speeds, color=['#2ecc71', '#e74c3c'])
        ax3.set_ylabel('MB/s')
        ax3.set_title('Velocidad de Escritura de Disco')
        ax3.grid(axis='y', alpha=0.3)
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

        ax4 = axes[1, 0]
        net_throughput = [virtio['network_throughput'], 
                         emulated['network_throughput']]
        bars4 = ax4.bar(categories, net_throughput, color=['#2ecc71', '#e74c3c'])
        ax4.set_ylabel('Mbps')
        ax4.set_title('Throughput de Red')
        ax4.grid(axis='y', alpha=0.3)
        for bar in bars4:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}',
                    ha='center', va='bottom')
  
        ax5 = axes[1, 1]
        cpu_overhead = [virtio['cpu_overhead'], emulated['cpu_overhead']]
        bars5 = ax5.bar(categories, cpu_overhead, color=['#2ecc71', '#e74c3c'])
        ax5.set_ylabel('Porcentaje (%)')
        ax5.set_title('Overhead de CPU')
        ax5.grid(axis='y', alpha=0.3)
        for bar in bars5:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')

        ax6 = axes[1, 2]
        improvements = {
            'Arranque': ((emulated['boot_time'] - virtio['boot_time']) / 
                        emulated['boot_time'] * 100),
            'Lectura': ((virtio['disk_read_speed'] - emulated['disk_read_speed']) / 
                       emulated['disk_read_speed'] * 100),
            'Escritura': ((virtio['disk_write_speed'] - emulated['disk_write_speed']) / 
                         emulated['disk_write_speed'] * 100),
            'Red': ((virtio['network_throughput'] - emulated['network_throughput']) / 
                   emulated['network_throughput'] * 100),
            'CPU': ((emulated['cpu_overhead'] - virtio['cpu_overhead']) / 
                   emulated['cpu_overhead'] * 100)
        }
        
        imp_categories = list(improvements.keys())
        imp_values = list(improvements.values())
        colors = ['#27ae60' if v > 0 else '#e67e22' for v in imp_values]
        bars6 = ax6.barh(imp_categories, imp_values, color=colors)
        ax6.set_xlabel('Mejora (%)')
        ax6.set_title('Mejora de Virtio sobre Emulado')
        ax6.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax6.grid(axis='x', alpha=0.3)
        for i, bar in enumerate(bars6):
            width = bar.get_width()
            ax6.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{width:.1f}%',
                    ha='left' if width > 0 else 'right',
                    va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('virtualization_comparison.png', dpi=300, bbox_inches='tight')
        print("[OK] Gráficos guardados en 'virtualization_comparison.png'")
        plt.show()
    
    def generate_detailed_report(self):
        if not self.data or 'metrics' not in self.data:
            print("[ERROR] Datos no disponibles")
            return
        
        metrics = self.data['metrics']
        virtio = metrics[0]
        emulated = metrics[1]
        
        report = []
        report.append("\n" + "="*80)
        report.append("ANÁLISIS DETALLADO: VIRTUALIZACIÓN DE E/S")
        report.append("="*80 + "\n")
        
        report.append("1. ANÁLISIS DE RENDIMIENTO DE DISCO")
        report.append("-" * 80)
        
        read_ratio = virtio['disk_read_speed'] / emulated['disk_read_speed']
        write_ratio = virtio['disk_write_speed'] / emulated['disk_write_speed']
        
        report.append(f"   Lectura:")
        report.append(f"      • Virtio: {virtio['disk_read_speed']:.2f} MB/s")
        report.append(f"      • Emulado: {emulated['disk_read_speed']:.2f} MB/s")
        report.append(f"      • Ratio: {read_ratio:.2f}x más rápido")
        report.append(f"      • Mejora: {(read_ratio - 1) * 100:.1f}%\n")
        
        report.append(f"   Escritura:")
        report.append(f"      • Virtio: {virtio['disk_write_speed']:.2f} MB/s")
        report.append(f"      • Emulado: {emulated['disk_write_speed']:.2f} MB/s")
        report.append(f"      • Ratio: {write_ratio:.2f}x más rápido")
        report.append(f"      • Mejora: {(write_ratio - 1) * 100:.1f}%\n")
        
        report.append(f"   Interpretación:")
        report.append(f"      Virtio utiliza paravirtualización, permitiendo al guest OS")
        report.append(f"      comunicarse directamente con el hypervisor mediante drivers")
        report.append(f"      optimizados. IDE requiere emulación completa del hardware.\n")

        report.append("\n2. ANÁLISIS DE RENDIMIENTO DE RED")
        report.append("-" * 80)
        
        net_ratio = virtio['network_throughput'] / emulated['network_throughput']
        
        report.append(f"   Throughput:")
        report.append(f"      • Virtio-net: {virtio['network_throughput']:.2f} Mbps")
        report.append(f"      • e1000: {emulated['network_throughput']:.2f} Mbps")
        report.append(f"      • Ratio: {net_ratio:.2f}x más rápido")
        report.append(f"      • Mejora: {(net_ratio - 1) * 100:.1f}%\n")
        
        report.append(f"   Interpretación:")
        report.append(f"      Virtio-net reduce el overhead eliminando la necesidad de")
        report.append(f"      emular completamente una tarjeta Intel e1000. Usa un modelo")
        report.append(f"      de cola compartida más eficiente.\n")

        report.append("\n3. ANÁLISIS DE TIEMPO DE ARRANQUE")
        report.append("-" * 80)
        
        boot_improvement = ((emulated['boot_time'] - virtio['boot_time']) / 
                           emulated['boot_time'] * 100)
        
        report.append(f"   Tiempo de arranque:")
        report.append(f"      • Virtio: {virtio['boot_time']:.3f} segundos")
        report.append(f"      • Emulado: {emulated['boot_time']:.3f} segundos")
        report.append(f"      • Diferencia: {emulated['boot_time'] - virtio['boot_time']:.3f} segundos")
        report.append(f"      • Mejora: {boot_improvement:.1f}%\n")
        
        report.append(f"   Interpretación:")
        report.append(f"      La detección y configuración de dispositivos virtio es más")
        report.append(f"      rápida ya que no requiere sondeo extensivo de hardware.\n")

        report.append("\n4. ANÁLISIS DE OVERHEAD DE CPU")
        report.append("-" * 80)
        
        cpu_reduction = ((emulated['cpu_overhead'] - virtio['cpu_overhead']) / 
                        emulated['cpu_overhead'] * 100)
        
        report.append(f"   Uso de CPU del host:")
        report.append(f"      • Virtio: {virtio['cpu_overhead']:.2f}%")
        report.append(f"      • Emulado: {emulated['cpu_overhead']:.2f}%")
        report.append(f"      • Reducción: {cpu_reduction:.1f}%\n")
        
        report.append(f"   Interpretación:")
        report.append(f"      La paravirtualización reduce ciclos de CPU necesarios para")
        report.append(f"      traducir operaciones de E/S, mejorando la densidad de VMs.\n")

        report.append("\n5. CONCLUSIONES Y RECOMENDACIONES")
        report.append("-" * 80)
        report.append("   • Virtio ofrece mejoras significativas en todos los aspectos medidos")
        report.append(f"   • Rendimiento de E/S mejora ~{((read_ratio + write_ratio) / 2 - 1) * 100:.0f}%")
        report.append(f"   • Throughput de red aumenta ~{(net_ratio - 1) * 100:.0f}%")
        report.append(f"   • Overhead de CPU se reduce ~{cpu_reduction:.0f}%")
        report.append("\n   Recomendaciones:")
        report.append("   1. Usar virtio para cargas de producción cuando sea posible")
        report.append("   2. Dispositivos emulados solo para compatibilidad legacy")
        report.append("   3. Considerar vhost-user para mayor rendimiento en red")
        report.append("   4. Implementar SR-IOV para E/S crítica en entornos cloud\n")
        
        report.append("="*80 + "\n")
        
        report_text = "\n".join(report)
        print(report_text)
        with open('detailed_analysis.txt', 'w') as f:
            f.write(report_text)
        print("[OK] Reporte detallado guardado en 'detailed_analysis.txt'")


def main():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║  ANALIZADOR DE VIRTUALIZACIÓN DE E/S            ║")
    print("╚══════════════════════════════════════════════════╝\n")
    
    try:
        analyzer = VirtualizationAnalyzer()
        
        print("[INFO] Generando análisis detallado...")
        analyzer.generate_detailed_report()
        
        print("\n[INFO] Generando visualizaciones...")
        analyzer.create_comparison_charts()
        
        print("\n[INFO] Análisis completado exitosamente")
        
    except Exception as e:
        print(f"[ERROR] Error durante análisis: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())