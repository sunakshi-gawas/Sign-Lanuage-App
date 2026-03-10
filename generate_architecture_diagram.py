"""
SignVerse AI System Architecture Diagram Generator
Generates a professional 2D academic-style architecture diagram in PNG format
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines
import numpy as np

# Set up figure with white background
fig, ax = plt.subplots(1, 1, figsize=(16, 12), facecolor='white')
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.set_aspect('equal')
ax.axis('off')

# Color palette (academic style - muted colors)
colors = {
    'mobile': '#D4E6F1',      # Light blue
    'backend': '#FADBD8',     # Light red/pink
    'ml': '#D5F5E3',          # Light green
    'data': '#F9E79F',        # Light yellow
    'box': '#FFFFFF',         # White for inner boxes
    'border': '#2C3E50',      # Dark gray for borders
    'arrow': '#34495E',       # Dark gray for arrows
    'text': '#1A1A1A'         # Almost black for text
}

def draw_box(ax, x, y, width, height, label, sublabel=None, color='white', border_color='black', fontsize=9):
    """Draw a rounded rectangle box with label"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=color, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(box)
    
    if sublabel:
        ax.text(x + width/2, y + height/2 + 0.15, label, 
                ha='center', va='center', fontsize=fontsize, fontweight='bold', color=colors['text'])
        ax.text(x + width/2, y + height/2 - 0.15, sublabel, 
                ha='center', va='center', fontsize=fontsize-2, color=colors['text'], style='italic')
    else:
        ax.text(x + width/2, y + height/2, label, 
                ha='center', va='center', fontsize=fontsize, fontweight='bold', color=colors['text'])

def draw_layer_box(ax, x, y, width, height, label, color):
    """Draw a layer container box"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02,rounding_size=0.2",
                         facecolor=color, edgecolor=colors['border'], linewidth=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height - 0.3, label, 
            ha='center', va='top', fontsize=11, fontweight='bold', color=colors['text'])

def draw_arrow(ax, start, end, label=None, bidirectional=False, style='->'):
    """Draw an arrow between two points"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=colors['arrow'], lw=1.5))
    if label:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x + 0.1, mid_y, label, fontsize=7, color=colors['text'], 
                ha='left', va='center', style='italic',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.8))

# ==================== TITLE ====================
ax.text(8, 11.5, 'SignVerse AI: System Architecture', 
        ha='center', va='center', fontsize=16, fontweight='bold', color=colors['text'])
ax.text(8, 11.1, 'Real-Time Sign Language Recognition and Translation System', 
        ha='center', va='center', fontsize=10, color='#666666', style='italic')

# ==================== MOBILE APPLICATION LAYER ====================
draw_layer_box(ax, 0.5, 7.5, 5.5, 3.3, 'Mobile Application Layer', colors['mobile'])
ax.text(3.25, 10.45, '(Flutter - Sign Bridge)', ha='center', va='center', fontsize=8, color='#666666')

# Mobile components
draw_box(ax, 0.8, 9.1, 2.3, 0.8, 'Camera Module', 'Video Capture', colors['box'], colors['border'])
draw_box(ax, 3.4, 9.1, 2.3, 0.8, 'MediaPipe', 'Hand Detection', colors['box'], colors['border'])
draw_box(ax, 0.8, 8.0, 2.3, 0.8, 'User Interface', 'Sign/Text Views', colors['box'], colors['border'])
draw_box(ax, 3.4, 8.0, 2.3, 0.8, 'TTS/GIF Player', 'Output Display', colors['box'], colors['border'])

# Arrows within mobile layer
draw_arrow(ax, (3.1, 9.5), (3.4, 9.5), '63 features')
draw_arrow(ax, (2.0, 9.1), (2.0, 8.8))
draw_arrow(ax, (4.5, 9.1), (4.5, 8.8))

# ==================== BACKEND SERVER LAYER ====================
draw_layer_box(ax, 0.5, 4.0, 5.5, 3.0, 'Backend Server Layer', colors['backend'])
ax.text(3.25, 6.65, '(FastAPI - Port 8000)', ha='center', va='center', fontsize=8, color='#666666')

# Backend components
draw_box(ax, 0.8, 5.5, 2.3, 0.8, 'REST API', 'Gateway', colors['box'], colors['border'])
draw_box(ax, 3.4, 5.5, 2.3, 0.8, 'Translator', 'Multi-language', colors['box'], colors['border'])
draw_box(ax, 0.8, 4.4, 2.3, 0.8, 'Sign-to-Text', 'Service', colors['box'], colors['border'])
draw_box(ax, 3.4, 4.4, 2.3, 0.8, 'Text-to-Sign', 'Service', colors['box'], colors['border'])

# Arrows within backend
draw_arrow(ax, (3.1, 5.9), (3.4, 5.9))
draw_arrow(ax, (1.95, 5.5), (1.95, 5.2))
draw_arrow(ax, (4.55, 5.5), (4.55, 5.2))

# ==================== ML INFERENCE LAYER ====================
draw_layer_box(ax, 7.0, 4.0, 8.5, 6.8, 'ML Inference Layer', colors['ml'])
ax.text(11.25, 10.45, '(TensorFlow - Port 8001)', ha='center', va='center', fontsize=8, color='#666666')

# Feature Processing
draw_box(ax, 7.4, 9.1, 2.3, 0.8, 'Feature Normalizer', 'Wrist-centered', colors['box'], colors['border'])
draw_box(ax, 10.0, 9.1, 2.3, 0.8, 'StandardScaler', 'Pre-fitted', colors['box'], colors['border'])

# DNN Architecture (main box)
draw_layer_box(ax, 7.4, 5.5, 7.8, 3.2, '', '#E8F6F3')
ax.text(11.3, 8.4, 'Deep Neural Network (DNN)', ha='center', va='center', fontsize=10, fontweight='bold', color=colors['text'])

# DNN layers
layers = [
    ('Input', '63', 7.8),
    ('Dense+BN', '512', 8.7),
    ('Dense+BN', '256', 9.6),
    ('Dense+BN', '128', 10.5),
    ('Dense+BN', '64', 11.4),
    ('Dense', '32', 12.3),
    ('Output', 'N', 13.2)
]

layer_y = 6.8
layer_height = 0.5
for label, units, lx in layers:
    box = FancyBboxPatch((lx, layer_y), 0.8, layer_height,
                         boxstyle="round,pad=0.01,rounding_size=0.08",
                         facecolor='#AED6F1' if label != 'Output' else '#ABEBC6', 
                         edgecolor=colors['border'], linewidth=1)
    ax.add_patch(box)
    ax.text(lx + 0.4, layer_y + layer_height/2 + 0.08, label, 
            ha='center', va='center', fontsize=6, fontweight='bold', color=colors['text'])
    ax.text(lx + 0.4, layer_y + layer_height/2 - 0.12, f'({units})', 
            ha='center', va='center', fontsize=5, color='#555')

# Connect DNN layers with arrows
for i in range(len(layers) - 1):
    ax.annotate('', xy=(layers[i+1][2], layer_y + layer_height/2), 
                xytext=(layers[i][2] + 0.8, layer_y + layer_height/2),
                arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1))

# Regularization labels
ax.text(9.2, 6.1, 'L2 Regularization + Dropout (0.2-0.4) + BatchNorm', 
        ha='center', va='center', fontsize=7, color='#666', style='italic')

ax.text(12.8, 6.1, 'Softmax', 
        ha='center', va='center', fontsize=7, color='#666', style='italic')

# Model and Label components
draw_box(ax, 7.4, 4.4, 2.3, 0.8, 'Trained Model', 'sign_model.h5', colors['box'], colors['border'])
draw_box(ax, 10.0, 4.4, 2.3, 0.8, 'Label Map', '14 Sign Classes', colors['box'], colors['border'])
draw_box(ax, 12.6, 4.4, 2.3, 0.8, 'Confidence', 'Threshold: 70%', colors['box'], colors['border'])

# Arrows in ML layer
draw_arrow(ax, (9.7, 9.5), (10.0, 9.5))
draw_arrow(ax, (11.15, 9.1), (11.15, 8.7))
draw_arrow(ax, (8.6, 5.5), (8.6, 5.2))
draw_arrow(ax, (11.15, 5.5), (11.15, 5.2))
draw_arrow(ax, (9.7, 4.8), (10.0, 4.8))
draw_arrow(ax, (12.3, 4.8), (12.6, 4.8))

# ==================== DATA STORAGE LAYER ====================
draw_layer_box(ax, 0.5, 0.8, 15.0, 2.8, 'Data Storage Layer', colors['data'])

# Data components
draw_box(ax, 1.0, 1.4, 2.5, 1.2, 'Training Data', '.npy Files\n(14 Signs × 900 Samples)', colors['box'], colors['border'], fontsize=8)
draw_box(ax, 4.0, 1.4, 2.5, 1.2, 'Sign GIFs', 'Animation Database', colors['box'], colors['border'], fontsize=8)
draw_box(ax, 7.0, 1.4, 2.5, 1.2, 'Model Weights', 'Keras H5 Format', colors['box'], colors['border'], fontsize=8)
draw_box(ax, 10.0, 1.4, 2.5, 1.2, 'Scaler Params', 'Pickle File', colors['box'], colors['border'], fontsize=8)
draw_box(ax, 13.0, 1.4, 2.2, 1.2, 'Label Mapping', 'JSON Config', colors['box'], colors['border'], fontsize=8)

# ==================== INTER-LAYER CONNECTIONS ====================
# Mobile to Backend
ax.annotate('', xy=(2.0, 7.0), xytext=(2.0, 7.5),
            arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=2))
ax.text(2.3, 7.25, 'HTTP/REST', fontsize=7, color='#E74C3C', fontweight='bold')

# Backend to ML
ax.annotate('', xy=(6.0, 5.0), xytext=(7.0, 5.0),
            arrowprops=dict(arrowstyle='<->', color='#E74C3C', lw=2))
ax.text(6.15, 5.25, 'Internal API', fontsize=7, color='#E74C3C', fontweight='bold')

# Backend to Data (GIFs)
ax.annotate('', xy=(4.55, 4.0), xytext=(5.25, 2.6),
            arrowprops=dict(arrowstyle='<->', color='#9B59B6', lw=1.5, 
                          connectionstyle='arc3,rad=-0.2'))

# ML to Data
ax.annotate('', xy=(8.25, 3.6), xytext=(8.25, 4.0),
            arrowprops=dict(arrowstyle='<-', color='#9B59B6', lw=1.5))
ax.annotate('', xy=(11.25, 3.6), xytext=(11.25, 4.0),
            arrowprops=dict(arrowstyle='<-', color='#9B59B6', lw=1.5))
ax.annotate('', xy=(14.1, 3.6), xytext=(14.1, 4.4),
            arrowprops=dict(arrowstyle='<-', color='#9B59B6', lw=1.5))

# Feature flow to ML
ax.annotate('', xy=(7.4, 9.5), xytext=(6.0, 8.4),
            arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2,
                          connectionstyle='arc3,rad=0.2'))
ax.text(6.5, 9.2, '63 Features', fontsize=7, color='#27AE60', fontweight='bold')

# ==================== LEGEND ====================
legend_x = 12.5
legend_y = 11.0
ax.text(legend_x, legend_y, 'Data Flow:', fontsize=8, fontweight='bold', color=colors['text'])

# Legend items
legend_items = [
    ('HTTP/REST', '#E74C3C'),
    ('Internal API', '#27AE60'),
    ('Data Access', '#9B59B6')
]

for i, (label, color) in enumerate(legend_items):
    y_pos = legend_y - 0.35 * (i + 1)
    ax.plot([legend_x, legend_x + 0.4], [y_pos, y_pos], color=color, linewidth=2)
    ax.text(legend_x + 0.5, y_pos, label, fontsize=7, color=colors['text'], va='center')

# ==================== SAVE ====================
plt.tight_layout()
plt.savefig('d:/Sign-Language-App-original/Sign-Language-App/system_architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print("System architecture diagram saved to: system_architecture.png")

# Also save as PDF for academic use
plt.savefig('d:/Sign-Language-App-original/Sign-Language-App/system_architecture.pdf', 
            bbox_inches='tight', facecolor='white', edgecolor='none')
print("PDF version saved to: system_architecture.pdf")

plt.show()
