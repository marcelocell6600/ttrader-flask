#!/usr/bin/env python3
"""
TTrader.com - Aplicação otimizada para mobile e desktop
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
import random
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app, origins="*")

# API Key para brapi.dev
BRAPI_API_KEY = "9GN5YztiAkoKu6f8ohNcz9"

# HTML inline otimizado para mobile
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>TTrader.com - Análise de Ações</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            color: #333; 
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            min-height: 100vh; 
            background: rgba(255, 255, 255, 0.95); 
            backdrop-filter: blur(10px); 
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.1); 
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); 
            color: white; 
            padding: 1rem; 
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1); 
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header-content { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            max-width: 1200px; 
            margin: 0 auto; 
        }
        .logo { display: flex; align-items: center; gap: 0.5rem; }
        .logo i { font-size: 1.8rem; color: #3498db; }
        .logo h1 { font-size: 1.5rem; font-weight: 700; }
        .logo .domain { font-size: 0.8rem; color: #3498db; font-weight: 400; }
        .nav { display: flex; gap: 1rem; }
        .nav-link { 
            color: rgba(255, 255, 255, 0.8); 
            text-decoration: none; 
            padding: 0.5rem 0.8rem; 
            border-radius: 8px; 
            transition: all 0.3s ease; 
            font-weight: 500; 
            cursor: pointer; 
            font-size: 0.9rem;
            white-space: nowrap;
        }
        .nav-link:hover, .nav-link.active { color: white; background: rgba(255, 255, 255, 0.1); }
        .main { padding: 1rem; max-width: 1200px; margin: 0 auto; }
        .section { display: none; animation: fadeIn 0.5s ease-in-out; }
        .section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .search-container { text-align: center; padding: 2rem 0; }
        .search-container h2 { font-size: 2rem; margin-bottom: 1rem; color: #2c3e50; font-weight: 700; }
        .subtitle { font-size: 1rem; color: #7f8c8d; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5; }
        .search-box { max-width: 600px; margin: 0 auto 2rem; position: relative; }
        .search-input-container { 
            display: flex; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); 
            overflow: hidden; 
            transition: all 0.3s ease; 
        }
        .search-input-container:focus-within { box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15); transform: translateY(-2px); }
        .search-icon { padding: 1rem; color: #7f8c8d; font-size: 1rem; }
        #stockSearch { 
            flex: 1; 
            border: none; 
            padding: 1rem 0; 
            font-size: 1rem; 
            outline: none; 
            background: transparent; 
        }
        .search-btn { 
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
            color: white; 
            border: none; 
            padding: 1rem 1.5rem; 
            font-size: 1rem; 
            font-weight: 600; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            min-width: 100px;
        }
        .search-btn:hover { background: linear-gradient(135deg, #2980b9 0%, #1f5f8b 100%); }
        .search-btn:active { transform: scale(0.98); }
        .popular-stocks h3 { margin-bottom: 1rem; color: #2c3e50; font-weight: 600; }
        .stock-chips { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); 
            gap: 0.5rem; 
            justify-content: center; 
            max-width: 500px;
            margin: 0 auto;
        }
        .stock-chip { 
            background: white; 
            border: 2px solid #3498db; 
            color: #3498db; 
            padding: 0.7rem 0.5rem; 
            border-radius: 12px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            font-weight: 600; 
            font-size: 0.9rem;
            text-align: center;
        }
        .stock-chip:hover, .stock-chip:active { 
            background: #3498db; 
            color: white; 
            transform: translateY(-2px); 
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3); 
        }
        .analysis-container { padding: 0.5rem 0; }
        .analysis-header { 
            display: flex; 
            align-items: flex-start; 
            gap: 1rem; 
            margin-bottom: 1.5rem; 
            padding-bottom: 1rem; 
            border-bottom: 2px solid #ecf0f1; 
            flex-wrap: wrap;
        }
        .back-btn { 
            background: #95a5a6; 
            color: white; 
            border: none; 
            padding: 0.7rem 1.2rem; 
            border-radius: 10px; 
            cursor: pointer; 
            transition: all 0.3s ease; 
            font-weight: 600; 
            font-size: 0.9rem;
            flex-shrink: 0;
        }
        .back-btn:hover { background: #7f8c8d; }
        .stock-info { flex: 1; min-width: 200px; }
        .stock-info h2 { font-size: 1.5rem; color: #2c3e50; margin-bottom: 0.5rem; }
        .stock-details { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
        .symbol { 
            background: #3498db; 
            color: white; 
            padding: 0.3rem 0.6rem; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 0.8rem; 
        }
        .price { font-size: 1.3rem; font-weight: 700; color: #2c3e50; }
        .change { 
            padding: 0.3rem 0.6rem; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 0.8rem; 
        }
        .change.positive { background: #2ecc71; color: white; }
        .change.negative { background: #e74c3c; color: white; }
        .analysis-grid { 
            display: grid; 
            grid-template-columns: 1fr; 
            gap: 1rem; 
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08); 
            overflow: hidden; 
            transition: all 0.3s ease; 
        }
        .card:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12); }
        .card-header { 
            padding: 1rem; 
            border-bottom: 1px solid #ecf0f1; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }
        .card-header h3 { color: #2c3e50; font-weight: 600; font-size: 1.1rem; }
        .chart-container { padding: 0.5rem; height: 250px; }
        .indicators-grid { 
            padding: 1rem; 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 1rem; 
        }
        .indicator { text-align: center; }
        .indicator-label { font-size: 0.8rem; color: #7f8c8d; margin-bottom: 0.3rem; font-weight: 500; }
        .indicator-value { font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.3rem; }
        .trend-content { padding: 1rem; }
        .trend-signal { text-align: center; margin-bottom: 1rem; }
        .signal-indicator { 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 0.5rem; 
            font-size: 1rem; 
            font-weight: 700; 
            margin-bottom: 0.8rem; 
            padding: 0.8rem; 
            border-radius: 12px; 
        }
        .signal-buy { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .signal-sell { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .signal-hold { background: linear-gradient(135deg, #f39c12, #e67e22); color: white; }
        .confidence-meter { margin-bottom: 0.8rem; }
        .confidence-label { font-size: 0.8rem; color: #7f8c8d; margin-bottom: 0.3rem; }
        .confidence-bar { 
            height: 8px; 
            background: #ecf0f1; 
            border-radius: 4px; 
            overflow: hidden; 
            margin-bottom: 0.3rem; 
        }
        .confidence-fill { 
            height: 100%; 
            background: linear-gradient(135deg, #3498db, #2980b9); 
            border-radius: 4px; 
            transition: width 0.5s ease; 
        }
        .confidence-value { font-weight: 600; color: #2c3e50; font-size: 0.9rem; }
        .trend-analysis { 
            background: #f8f9fa; 
            padding: 0.8rem; 
            border-radius: 10px; 
            font-size: 0.85rem; 
            line-height: 1.4; 
            color: #2c3e50; 
        }
        .sr-levels { padding: 1rem; display: grid; gap: 0.8rem; }
        .sr-level { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 0.8rem; 
            border-radius: 10px; 
            font-weight: 600; 
            font-size: 0.9rem;
        }
        .sr-level.resistance { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .sr-level.current { background: linear-gradient(135deg, #3498db, #2980b9); color: white; }
        .sr-level.support { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .recommendations-container { padding: 0.5rem 0; }
        .recommendations-header { text-align: center; margin-bottom: 1.5rem; }
        .recommendations-header h2 { font-size: 1.8rem; color: #2c3e50; margin-bottom: 0.5rem; }
        .recommendations-subtitle { color: #7f8c8d; font-size: 1rem; }
        .recommendations-content { display: grid; gap: 1rem; }
        .recommendation-card { 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08); 
            overflow: hidden; 
            transition: all 0.3s ease; 
        }
        .recommendation-card:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12); }
        .recommendation-header { 
            padding: 1rem; 
            background: linear-gradient(135deg, #3498db, #2980b9); 
            color: white; 
        }
        .recommendation-type { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.3rem; }
        .recommendation-strategy { font-size: 0.85rem; opacity: 0.9; }
        .recommendation-body { padding: 1rem; }
        .recommendation-details { display: grid; gap: 0.8rem; margin-bottom: 0.8rem; }
        .detail-item { 
            display: flex; 
            justify-content: space-between; 
            align-items: flex-start; 
            padding: 0.4rem 0; 
            border-bottom: 1px solid #ecf0f1; 
            gap: 0.5rem;
        }
        .detail-label { font-weight: 600; color: #7f8c8d; font-size: 0.85rem; flex-shrink: 0; }
        .detail-value { color: #2c3e50; font-weight: 600; font-size: 0.85rem; text-align: right; }
        .risk-level { 
            padding: 0.2rem 0.6rem; 
            border-radius: 10px; 
            font-size: 0.75rem; 
            font-weight: 600; 
        }
        .risk-low { background: #2ecc71; color: white; }
        .risk-medium { background: #f39c12; color: white; }
        .risk-high { background: #e74c3c; color: white; }
        .recommendation-description { 
            background: #f8f9fa; 
            padding: 0.8rem; 
            border-radius: 10px; 
            font-size: 0.85rem; 
            line-height: 1.4; 
            color: #2c3e50; 
        }
        .no-data { text-align: center; padding: 2rem; color: #7f8c8d; }
        .no-data i { font-size: 2.5rem; margin-bottom: 0.8rem; opacity: 0.5; }
        .loading-overlay { 
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background: rgba(0, 0, 0, 0.7); 
            display: none; 
            justify-content: center; 
            align-items: center; 
            z-index: 9999; 
        }
        .loading-spinner { text-align: center; color: white; }
        .loading-spinner i { font-size: 2.5rem; margin-bottom: 0.8rem; }
        .loading-spinner p { font-size: 1.1rem; }
        .error-message { 
            background: #e74c3c; 
            color: white; 
            padding: 0.8rem; 
            border-radius: 10px; 
            margin: 0.8rem 0; 
            text-align: center; 
            font-size: 0.9rem;
        }
        .footer-brand { 
            text-align: center; 
            padding: 1.5rem; 
            color: #7f8c8d; 
            font-size: 0.85rem; 
            border-top: 1px solid #ecf0f1; 
            margin-top: 2rem; 
        }
        .footer-brand strong { color: #3498db; }

        /* Mobile Optimizations */
        @media (max-width: 768px) { 
            .header { padding: 0.8rem; }
            .header-content { flex-direction: column; gap: 0.8rem; align-items: stretch; }
            .logo { justify-content: center; }
            .logo h1 { font-size: 1.3rem; }
            .nav { justify-content: center; gap: 0.5rem; }
            .nav-link { padding: 0.4rem 0.6rem; font-size: 0.85rem; }
            .main { padding: 0.8rem; }
            .search-container { padding: 1.5rem 0; }
            .search-container h2 { font-size: 1.6rem; }
            .subtitle { font-size: 0.9rem; }
            .search-input-container { flex-direction: column; }
            .search-btn { border-radius: 0 0 15px 15px; padding: 1rem; }
            .stock-chips { grid-template-columns: repeat(4, 1fr); gap: 0.4rem; }
            .stock-chip { padding: 0.6rem 0.3rem; font-size: 0.8rem; }
            .analysis-header { flex-direction: column; align-items: stretch; gap: 0.8rem; }
            .stock-info h2 { font-size: 1.3rem; }
            .stock-details { flex-direction: column; align-items: flex-start; gap: 0.4rem; }
            .price { font-size: 1.2rem; }
            .chart-container { height: 200px; padding: 0.3rem; }
            .indicators-grid { grid-template-columns: 1fr; gap: 0.8rem; }
            .indicator-value { font-size: 1.2rem; }
            .signal-indicator { font-size: 0.9rem; padding: 0.7rem; }
            .recommendations-header h2 { font-size: 1.5rem; }
            .detail-item { flex-direction: column; align-items: flex-start; gap: 0.2rem; }
            .detail-value { text-align: left; }
        }

        @media (max-width: 480px) {
            .header { padding: 0.6rem; }
            .logo h1 { font-size: 1.2rem; }
            .nav-link { padding: 0.3rem 0.5rem; font-size: 0.8rem; }
            .main { padding: 0.6rem; }
            .search-container h2 { font-size: 1.4rem; }
            .stock-chips { grid-template-columns: repeat(3, 1fr); }
            .stock-chip { padding: 0.5rem 0.2rem; font-size: 0.75rem; }
            .chart-container { height: 180px; }
            .card-header h3 { font-size: 1rem; }
        }

        /* Desktop Optimizations */
        @media (min-width: 1024px) {
            .analysis-grid { 
                grid-template-columns: 2fr 1fr; 
                grid-template-rows: auto auto; 
            }
            .chart-card { grid-row: span 2; }
            .chart-container { height: 400px; padding: 1rem; }
            .stock-chips { 
                display: flex; 
                flex-wrap: wrap; 
                justify-content: center; 
            }
            .stock-chip { min-width: 80px; }
        }

        /* Touch Optimizations */
        @media (hover: none) and (pointer: coarse) {
            .stock-chip:hover { transform: none; box-shadow: none; }
            .card:hover { transform: none; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08); }
            .recommendation-card:hover { transform: none; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08); }
        }

        /* High DPI Displays */
        @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
            .logo i { font-size: 1.9rem; }
            .search-icon { font-size: 1.1rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-chart-line"></i>
                    <div>
                        <h1>TTrader</h1>
                        <div class="domain">.com</div>
                    </div>
                </div>
                <nav class="nav">
                    <a href="#home" class="nav-link active" onclick="showSection('home')">Início</a>
                    <a href="#analysis" class="nav-link" onclick="showSection('analysis')">Análise</a>
                    <a href="#recommendations" class="nav-link" onclick="showSection('recommendations')">Recomendações</a>
                </nav>
            </div>
        </header>

        <main class="main">
            <section id="home" class="section active">
                <div class="search-container">
                    <h2>Análise Técnica de Ações</h2>
                    <p class="subtitle">Digite o código da ação para obter análise detalhada e recomendações para opções</p>
                    
                    <div class="search-box">
                        <div class="search-input-container">
                            <i class="fas fa-search search-icon"></i>
                            <input type="text" id="stockSearch" placeholder="Digite o código da ação (ex: PETR4, VALE3, ABEV3)" autocomplete="off">
                            <button id="searchBtn" class="search-btn" onclick="performSearch()">
                                <span class="btn-text">Analisar</span>
                            </button>
                        </div>
                    </div>

                    <div class="popular-stocks">
                        <h3>Ações Populares</h3>
                        <div class="stock-chips">
                            <button class="stock-chip" onclick="searchStock('PETR4')">PETR4</button>
                            <button class="stock-chip" onclick="searchStock('VALE3')">VALE3</button>
                            <button class="stock-chip" onclick="searchStock('ITUB4')">ITUB4</button>
                            <button class="stock-chip" onclick="searchStock('BBDC4')">BBDC4</button>
                            <button class="stock-chip" onclick="searchStock('ABEV3')">ABEV3</button>
                            <button class="stock-chip" onclick="searchStock('WEGE3')">WEGE3</button>
                            <button class="stock-chip" onclick="searchStock('MGLU3')">MGLU3</button>
                            <button class="stock-chip" onclick="searchStock('B3SA3')">B3SA3</button>
                        </div>
                    </div>
                </div>
                
                <div class="footer-brand">
                    <strong>TTrader.com</strong> - Sua plataforma de análise técnica para operações de opções
                </div>
            </section>

            <section id="analysis" class="section">
                <div class="analysis-container">
                    <div class="analysis-header">
                        <button class="back-btn" onclick="showSection('home')">
                            <i class="fas fa-arrow-left"></i>
                            Voltar
                        </button>
                        <div class="stock-info">
                            <h2 id="stockName">-</h2>
                            <div class="stock-details">
                                <span id="stockSymbol" class="symbol">-</span>
                                <span id="stockPrice" class="price">R$ -</span>
                                <span id="stockChange" class="change">-</span>
                            </div>
                        </div>
                    </div>

                    <div class="analysis-grid">
                        <div class="card chart-card">
                            <div class="card-header">
                                <h3>Gráfico de Preços</h3>
                            </div>
                            <div class="chart-container">
                                <canvas id="priceChart"></canvas>
                            </div>
                        </div>

                        <div class="card indicators-card">
                            <div class="card-header">
                                <h3>Indicadores Técnicos</h3>
                            </div>
                            <div class="indicators-grid">
                                <div class="indicator">
                                    <div class="indicator-label">RSI (14)</div>
                                    <div class="indicator-value" id="rsiValue">-</div>
                                </div>
                                <div class="indicator">
                                    <div class="indicator-label">MACD</div>
                                    <div class="indicator-value" id="macdValue">-</div>
                                </div>
                            </div>
                        </div>

                        <div class="card trend-card">
                            <div class="card-header">
                                <h3>Análise de Tendência</h3>
                            </div>
                            <div class="trend-content">
                                <div class="trend-signal">
                                    <div class="signal-indicator" id="trendSignal">
                                        <i class="fas fa-minus"></i>
                                        <span>AGUARDAR</span>
                                    </div>
                                    <div class="confidence-meter">
                                        <div class="confidence-label">Confiança</div>
                                        <div class="confidence-bar">
                                            <div class="confidence-fill" id="confidenceFill"></div>
                                        </div>
                                        <div class="confidence-value" id="confidenceValue">0%</div>
                                    </div>
                                </div>
                                <div class="trend-analysis" id="trendAnalysis">
                                    Aguardando análise...
                                </div>
                            </div>
                        </div>

                        <div class="card support-resistance-card">
                            <div class="card-header">
                                <h3>Suporte e Resistência</h3>
                            </div>
                            <div class="sr-levels">
                                <div class="sr-level resistance">
                                    <div class="sr-label">Resistência</div>
                                    <div class="sr-value" id="resistanceValue">R$ -</div>
                                </div>
                                <div class="sr-level current">
                                    <div class="sr-label">Preço Atual</div>
                                    <div class="sr-value" id="currentPriceValue">R$ -</div>
                                </div>
                                <div class="sr-level support">
                                    <div class="sr-label">Suporte</div>
                                    <div class="sr-value" id="supportValue">R$ -</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="recommendations" class="section">
                <div class="recommendations-container">
                    <div class="recommendations-header">
                        <h2>Recomendações para Opções</h2>
                        <p class="recommendations-subtitle">Estratégias baseadas na análise técnica atual</p>
                    </div>

                    <div id="recommendationsContent" class="recommendations-content">
                        <div class="no-data">
                            <i class="fas fa-chart-bar"></i>
                            <p>Realize uma análise primeiro para ver as recomendações</p>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <div id="loadingOverlay" class="loading-overlay">
            <div class="loading-spinner">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Analisando ação...</p>
            </div>
        </div>
    </div>

    <script>
        let currentStock = null;
        let priceChart = null;

        // Mobile optimizations
        function isMobile() {
            return window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        }

        function showSection(sectionId) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + sectionId) {
                    link.classList.add('active');
                }
            });
            
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
                if (section.id === sectionId) {
                    section.classList.add('active');
                }
            });

            // Scroll to top on mobile when changing sections
            if (isMobile()) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        function searchStock(symbol) {
            document.getElementById('stockSearch').value = symbol;
            performSearch();
        }

        async function performSearch() {
            const symbol = document.getElementById('stockSearch').value.trim().toUpperCase();
            
            if (!symbol) {
                alert('Por favor, digite o código de uma ação.');
                return;
            }
            
            showLoading(true);
            
            try {
                const analysisResponse = await fetch('/api/stocks/analysis/' + symbol);
                const analysisData = await analysisResponse.json();
                
                if (!analysisResponse.ok) {
                    throw new Error(analysisData.error || 'Erro ao buscar dados da ação');
                }
                
                const recommendationsResponse = await fetch('/api/stocks/recommendations/' + symbol);
                const recommendationsData = await recommendationsResponse.json();
                
                currentStock = {
                    symbol: symbol,
                    analysis: analysisData,
                    recommendations: recommendationsData
                };
                
                updateStockInfo(analysisData);
                updateTechnicalIndicators(analysisData.technical_indicators);
                updateTrendAnalysis(analysisData.trend_analysis);
                updateSupportResistance(analysisData.support_resistance, analysisData.current_quote);
                updateRecommendations(recommendationsData.recommendations);
                updateChart(symbol);
                
                showSection('analysis');
                
            } catch (error) {
                console.error('Analysis error:', error);
                alert(error.message || 'Erro ao analisar a ação. Verifique se o código está correto e tente novamente.');
            } finally {
                showLoading(false);
            }
        }

        function updateStockInfo(data) {
            const quote = data.current_quote;
            
            document.getElementById('stockName').textContent = quote?.longName || quote?.shortName || data.symbol;
            document.getElementById('stockSymbol').textContent = data.symbol;
            
            if (quote?.regularMarketPrice) {
                document.getElementById('stockPrice').textContent = 'R$ ' + quote.regularMarketPrice.toFixed(2);
                
                if (quote.regularMarketChange !== undefined && quote.regularMarketChangePercent !== undefined) {
                    const changeElement = document.getElementById('stockChange');
                    const changeValue = quote.regularMarketChange >= 0 ? '+' + quote.regularMarketChange.toFixed(2) : quote.regularMarketChange.toFixed(2);
                    const changePercent = quote.regularMarketChangePercent >= 0 ? '+' + quote.regularMarketChangePercent.toFixed(2) + '%' : quote.regularMarketChangePercent.toFixed(2) + '%';
                    
                    changeElement.textContent = changeValue + ' (' + changePercent + ')';
                    changeElement.className = 'change ' + (quote.regularMarketChange >= 0 ? 'positive' : 'negative');
                }
            }
        }

        function updateTechnicalIndicators(indicators) {
            if (indicators.rsi !== null && indicators.rsi !== undefined) {
                document.getElementById('rsiValue').textContent = indicators.rsi.toFixed(1);
            }
            
            if (indicators.macd !== null && indicators.macd !== undefined) {
                document.getElementById('macdValue').textContent = indicators.macd.toFixed(4);
            }
        }

        function updateTrendAnalysis(trendData) {
            const signalElement = document.getElementById('trendSignal');
            const confidenceFill = document.getElementById('confidenceFill');
            const confidenceValue = document.getElementById('confidenceValue');
            const analysisText = document.getElementById('trendAnalysis');
            
            signalElement.className = 'signal-indicator signal-' + trendData.signal.toLowerCase();
            
            let icon, text;
            switch (trendData.signal) {
                case 'BUY':
                    icon = 'fas fa-arrow-up';
                    text = 'COMPRAR';
                    break;
                case 'SELL':
                    icon = 'fas fa-arrow-down';
                    text = 'VENDER';
                    break;
                default:
                    icon = 'fas fa-minus';
                    text = 'AGUARDAR';
            }
            
            signalElement.innerHTML = '<i class="' + icon + '"></i><span>' + text + '</span>';
            
            confidenceFill.style.width = trendData.confidence + '%';
            confidenceValue.textContent = trendData.confidence.toFixed(1) + '%';
            
            analysisText.textContent = trendData.analysis;
        }

        function updateSupportResistance(srData, quote) {
            const currentPrice = quote?.regularMarketPrice;
            
            document.getElementById('resistanceValue').textContent = 
                srData.resistance ? 'R$ ' + srData.resistance.toFixed(2) : 'N/A';
            
            document.getElementById('currentPriceValue').textContent = 
                currentPrice ? 'R$ ' + currentPrice.toFixed(2) : 'N/A';
            
            document.getElementById('supportValue').textContent = 
                srData.support ? 'R$ ' + srData.support.toFixed(2) : 'N/A';
        }

        function updateRecommendations(recommendations) {
            const container = document.getElementById('recommendationsContent');
            
            if (!recommendations || recommendations.length === 0) {
                container.innerHTML = '<div class="no-data"><i class="fas fa-chart-bar"></i><p>Nenhuma recomendação disponível para esta ação no momento.</p></div>';
                return;
            }
            
            const html = recommendations.map(rec => 
                '<div class="recommendation-card">' +
                    '<div class="recommendation-header">' +
                        '<div class="recommendation-type">' + rec.type + '</div>' +
                        '<div class="recommendation-strategy">' + rec.strategy + '</div>' +
                    '</div>' +
                    '<div class="recommendation-body">' +
                        '<div class="recommendation-details">' +
                            '<div class="detail-item">' +
                                '<span class="detail-label">Strike Sugerido:</span>' +
                                '<span class="detail-value">' + rec.strike_suggestion + '</span>' +
                            '</div>' +
                            '<div class="detail-item">' +
                                '<span class="detail-label">Vencimento:</span>' +
                                '<span class="detail-value">' + rec.expiration + '</span>' +
                            '</div>' +
                            '<div class="detail-item">' +
                                '<span class="detail-label">Nível de Risco:</span>' +
                                '<span class="detail-value">' +
                                    '<span class="risk-level risk-' + rec.risk_level.toLowerCase() + '">' + rec.risk_level + '</span>' +
                                '</span>' +
                            '</div>' +
                        '</div>' +
                        '<div class="recommendation-description">' + rec.description + '</div>' +
                    '</div>' +
                '</div>'
            ).join('');
            
            container.innerHTML = html;
        }

        async function updateChart(symbol) {
            try {
                const response = await fetch('/api/stocks/chart/' + symbol);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao carregar dados do gráfico');
                }
                
                renderChart(data.data);
                
            } catch (error) {
                console.error('Chart error:', error);
            }
        }

        function renderChart(chartData) {
            const ctx = document.getElementById('priceChart').getContext('2d');
            
            if (priceChart) {
                priceChart.destroy();
            }
            
            const labels = chartData.map(item => new Date(item.date));
            const prices = chartData.map(item => item.close);
            
            // Mobile-optimized chart configuration
            const chartConfig = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Preço',
                        data: prices,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: isMobile() ? 1.5 : 2,
                        fill: false,
                        tension: 0.1,
                        pointRadius: isMobile() ? 1 : 2,
                        pointHoverRadius: isMobile() ? 3 : 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    plugins: {
                        legend: {
                            display: !isMobile(),
                            labels: {
                                font: {
                                    size: isMobile() ? 10 : 12
                                }
                            }
                        },
                        tooltip: {
                            titleFont: {
                                size: isMobile() ? 10 : 12
                            },
                            bodyFont: {
                                size: isMobile() ? 10 : 12
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                displayFormats: {
                                    day: isMobile() ? 'dd/MM' : 'dd/MM/yyyy'
                                }
                            },
                            ticks: {
                                font: {
                                    size: isMobile() ? 9 : 11
                                },
                                maxTicksLimit: isMobile() ? 6 : 10
                            }
                        },
                        y: {
                            beginAtZero: false,
                            ticks: {
                                font: {
                                    size: isMobile() ? 9 : 11
                                },
                                callback: function(value) {
                                    return 'R$ ' + value.toFixed(2);
                                }
                            }
                        }
                    }
                }
            };
            
            priceChart = new Chart(ctx, chartConfig);
        }

        function showLoading(show) {
            document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
        }

        // Event listeners
        document.getElementById('stockSearch').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // Touch event optimizations for mobile
        if (isMobile()) {
            document.addEventListener('touchstart', function() {}, { passive: true });
            
            // Prevent zoom on double tap for input fields
            document.getElementById('stockSearch').addEventListener('touchend', function(e) {
                e.preventDefault();
                this.focus();
            });
        }

        // Resize handler for chart responsiveness
        window.addEventListener('resize', function() {
            if (priceChart) {
                priceChart.resize();
            }
        });

        // Prevent horizontal scroll on mobile
        document.addEventListener('touchmove', function(e) {
            if (e.touches.length > 1) {
                e.preventDefault();
            }
        }, { passive: false });
    </script>
</body>
</html>'''

def get_stock_data_brapi(symbol):
    """Busca dados da ação na API brapi.dev com API key"""
    try:
        # Adicionar .SA se não tiver
        if not symbol.endswith('.SA'):
            symbol_sa = symbol + '.SA'
        else:
            symbol_sa = symbol
            
        url = f"https://brapi.dev/api/quote/{symbol_sa}?token={BRAPI_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                return data['results'][0]
        
        return None
    except Exception as e:
        print(f"Erro ao buscar dados na brapi: {e}")
        return None

def calculate_simple_indicators(symbol):
    """Calcula indicadores técnicos simples usando dados da brapi com API key"""
    try:
        # Buscar dados históricos da brapi
        if not symbol.endswith('.SA'):
            symbol_sa = symbol + '.SA'
        else:
            symbol_sa = symbol
            
        url = f"https://brapi.dev/api/quote/{symbol_sa}?range=3mo&interval=1d&token={BRAPI_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        if 'results' not in data or len(data['results']) == 0:
            return None
            
        result = data['results'][0]
        historical_data = result.get('historicalDataPrice', [])
        
        if len(historical_data) < 20:
            return None
        
        # Extrair preços de fechamento
        closes = [float(item['close']) for item in historical_data]
        
        # Calcular RSI simples (14 períodos)
        def calculate_rsi(prices, window=14):
            if len(prices) < window + 1:
                return None
            
            gains = []
            losses = []
            
            for i in range(1, len(prices)):
                change = prices[i] - prices[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
            
            if len(gains) < window:
                return None
                
            avg_gain = sum(gains[-window:]) / window
            avg_loss = sum(losses[-window:]) / window
            
            if avg_loss == 0:
                return 100
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        
        # Calcular MACD simples
        def calculate_simple_macd(prices, fast=12, slow=26):
            if len(prices) < slow:
                return None, None
                
            # EMA simples
            def ema(data, span):
                alpha = 2 / (span + 1)
                ema_values = [data[0]]
                for i in range(1, len(data)):
                    ema_values.append(alpha * data[i] + (1 - alpha) * ema_values[-1])
                return ema_values
            
            ema_fast = ema(prices, fast)
            ema_slow = ema(prices, slow)
            
            macd = ema_fast[-1] - ema_slow[-1]
            
            # MACD signal line (EMA 9 do MACD)
            macd_line = [ema_fast[i] - ema_slow[i] for i in range(len(ema_slow))]
            signal_line = ema(macd_line, 9)
            
            return macd, signal_line[-1]
        
        rsi = calculate_rsi(closes)
        macd, macd_signal = calculate_simple_macd(closes)
        
        # Médias móveis simples
        sma_20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else None
        sma_50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else None
        
        return {
            'rsi': rsi,
            'macd': macd,
            'macd_signal': macd_signal,
            'sma_20': sma_20,
            'sma_50': sma_50
        }
        
    except Exception as e:
        print(f"Erro ao calcular indicadores: {e}")
        return None

def analyze_trend(indicators, current_price):
    """Analisa tendência baseada nos indicadores técnicos"""
    if not indicators:
        return {
            'signal': 'HOLD',
            'confidence': 50.0,
            'analysis': 'Dados insuficientes para análise.'
        }
    
    signals = []
    
    # Análise RSI
    rsi = indicators.get('rsi')
    if rsi:
        if rsi < 30:
            signals.append('BUY')
        elif rsi > 70:
            signals.append('SELL')
        else:
            signals.append('HOLD')
    
    # Análise MACD
    macd = indicators.get('macd')
    macd_signal = indicators.get('macd_signal')
    if macd and macd_signal:
        if macd > macd_signal:
            signals.append('BUY')
        else:
            signals.append('SELL')
    
    # Análise Médias Móveis
    sma_20 = indicators.get('sma_20')
    sma_50 = indicators.get('sma_50')
    if sma_20 and sma_50:
        if sma_20 > sma_50:
            signals.append('BUY')
        else:
            signals.append('SELL')
    
    # Determinar sinal final
    buy_count = signals.count('BUY')
    sell_count = signals.count('SELL')
    
    if buy_count > sell_count:
        signal = 'BUY'
        confidence = min(90, 60 + (buy_count - sell_count) * 10)
    elif sell_count > buy_count:
        signal = 'SELL'
        confidence = min(90, 60 + (sell_count - buy_count) * 10)
    else:
        signal = 'HOLD'
        confidence = 50.0
    
    # Gerar análise textual
    analysis_text = ""
    if rsi:
        analysis_text += f"RSI em {rsi:.1f} "
        if rsi < 30:
            analysis_text += "indica ativo sobrevendido. "
        elif rsi > 70:
            analysis_text += "indica ativo sobrecomprado. "
        else:
            analysis_text += "está em zona neutra. "
    
    if macd and macd_signal:
        analysis_text += f"MACD {'acima' if macd > macd_signal else 'abaixo'} da linha de sinal. "
    
    analysis_text += f"Sinais técnicos sugerem {signal.lower()} com {confidence:.1f}% de confiança."
    
    return {
        'signal': signal,
        'confidence': confidence,
        'analysis': analysis_text
    }

@app.route('/')
def serve_index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stocks/search')
def search_stocks():
    query = request.args.get('q', '').upper()
    
    # Lista expandida de ações populares para busca rápida
    popular_stocks = [
        {'symbol': 'PETR4', 'name': 'Petróleo Brasileiro S.A. - Petrobras'},
        {'symbol': 'VALE3', 'name': 'Vale S.A.'},
        {'symbol': 'ITUB4', 'name': 'Itaú Unibanco Holding S.A.'},
        {'symbol': 'BBDC4', 'name': 'Banco Bradesco S.A.'},
        {'symbol': 'ABEV3', 'name': 'Ambev S.A.'},
        {'symbol': 'WEGE3', 'name': 'WEG S.A.'},
        {'symbol': 'MGLU3', 'name': 'Magazine Luiza S.A.'},
        {'symbol': 'B3SA3', 'name': 'B3 S.A. - Brasil, Bolsa, Balcão'},
        {'symbol': 'RENT3', 'name': 'Localiza Rent a Car S.A.'},
        {'symbol': 'LREN3', 'name': 'Lojas Renner S.A.'},
        {'symbol': 'SUZB3', 'name': 'Suzano S.A.'},
        {'symbol': 'JBSS3', 'name': 'JBS S.A.'},
        {'symbol': 'EMBR3', 'name': 'Embraer S.A.'},
        {'symbol': 'CSAN3', 'name': 'Cosan S.A.'},
        {'symbol': 'RADL3', 'name': 'Raia Drogasil S.A.'},
        {'symbol': 'HAPV3', 'name': 'Hapvida Participações e Investimentos S.A.'},
        {'symbol': 'RAIL3', 'name': 'Rumo S.A.'},
        {'symbol': 'CCRO3', 'name': 'CCR S.A.'},
        {'symbol': 'GGBR4', 'name': 'Gerdau S.A.'},
        {'symbol': 'USIM5', 'name': 'Usinas Siderúrgicas de Minas Gerais S.A.'}
    ]
    
    results = []
    for stock in popular_stocks:
        if query in stock['symbol'] or query in stock['name'].upper():
            results.append(stock)
    
    return jsonify({'results': results})

@app.route('/api/stocks/quote/<symbol>')
def get_quote(symbol):
    symbol = symbol.upper()
    
    stock_data = get_stock_data_brapi(symbol)
    
    if stock_data:
        return jsonify(stock_data)
    else:
        return jsonify({'error': 'Ação não encontrada'}), 404

@app.route('/api/stocks/analysis/<symbol>')
def get_analysis(symbol):
    symbol = symbol.upper()
    
    # Buscar dados da ação
    stock_data = get_stock_data_brapi(symbol)
    
    if not stock_data:
        return jsonify({'error': 'Ação não encontrada'}), 404
    
    # Calcular indicadores técnicos
    indicators = calculate_simple_indicators(symbol)
    
    # Obter preço atual
    current_price = stock_data.get('regularMarketPrice', 0)
    
    # Analisar tendência
    trend_analysis = analyze_trend(indicators, current_price)
    
    # Calcular suporte e resistência (aproximação simples)
    support = current_price * 0.95
    resistance = current_price * 1.05
    
    analysis_data = {
        'symbol': symbol,
        'current_quote': stock_data,
        'analysis_date': datetime.now().isoformat(),
        'trend_analysis': trend_analysis,
        'support_resistance': {
            'support': round(support, 2),
            'resistance': round(resistance, 2)
        },
        'technical_indicators': indicators or {},
        'historical_data': {
            'period': '3mo',
            'interval': '1d',
            'last_update': datetime.now().isoformat()
        }
    }
    
    return jsonify(analysis_data)

@app.route('/api/stocks/recommendations/<symbol>')
def get_recommendations(symbol):
    symbol = symbol.upper()
    
    # Buscar dados da ação
    stock_data = get_stock_data_brapi(symbol)
    
    if not stock_data:
        return jsonify({'error': 'Ação não encontrada'}), 404
    
    current_price = stock_data.get('regularMarketPrice', 0)
    
    # Calcular indicadores para determinar tendência
    indicators = calculate_simple_indicators(symbol)
    trend_analysis = analyze_trend(indicators, current_price)
    
    recommendations = []
    
    if trend_analysis['signal'] == 'BUY':
        recommendations = [
            {
                'type': 'CALL',
                'strategy': 'Compra de Call',
                'strike_suggestion': f"Strike próximo a R$ {current_price * 1.02:.2f} (2% OTM)",
                'expiration': '30-45 dias',
                'risk_level': 'Médio',
                'max_risk': 'Prêmio pago',
                'profit_potential': 'Ilimitado',
                'description': 'Estratégia para lucrar com alta do ativo'
            },
            {
                'type': 'PUT_SELL',
                'strategy': 'Venda de Put',
                'strike_suggestion': f"Strike próximo a R$ {current_price * 0.95:.2f} (5% OTM)",
                'expiration': '15-30 dias',
                'risk_level': 'Alto',
                'max_risk': 'Obrigação de comprar o ativo',
                'profit_potential': 'Prêmio recebido',
                'description': 'Estratégia para gerar renda com viés de alta'
            }
        ]
    elif trend_analysis['signal'] == 'SELL':
        recommendations = [
            {
                'type': 'PUT',
                'strategy': 'Compra de Put',
                'strike_suggestion': f"Strike próximo a R$ {current_price * 0.98:.2f} (2% OTM)",
                'expiration': '30-45 dias',
                'risk_level': 'Médio',
                'max_risk': 'Prêmio pago',
                'profit_potential': 'Alto potencial de lucro',
                'description': 'Estratégia para lucrar com queda do ativo'
            },
            {
                'type': 'CALL_SELL',
                'strategy': 'Venda de Call',
                'strike_suggestion': f"Strike próximo a R$ {current_price * 1.05:.2f} (5% OTM)",
                'expiration': '15-30 dias',
                'risk_level': 'Alto',
                'max_risk': 'Obrigação de vender o ativo',
                'profit_potential': 'Prêmio recebido',
                'description': 'Estratégia para gerar renda com viés de baixa'
            }
        ]
    else:
        recommendations = [
            {
                'type': 'IRON_CONDOR',
                'strategy': 'Iron Condor',
                'strike_suggestion': f"Calls: R$ {current_price * 1.05:.2f} / R$ {current_price * 1.10:.2f}, Puts: R$ {current_price * 0.95:.2f} / R$ {current_price * 0.90:.2f}",
                'expiration': '15-30 dias',
                'risk_level': 'Médio',
                'max_risk': 'Diferença entre strikes - crédito recebido',
                'profit_potential': 'Crédito líquido recebido',
                'description': 'Estratégia para mercado lateral'
            }
        ]
    
    return jsonify({
        'symbol': symbol,
        'current_price': current_price,
        'trend_signal': trend_analysis['signal'],
        'confidence': trend_analysis['confidence'],
        'support': round(current_price * 0.95, 2),
        'resistance': round(current_price * 1.05, 2),
        'recommendations': recommendations,
        'analysis_summary': trend_analysis['analysis']
    })

@app.route('/api/stocks/chart/<symbol>')
def get_chart_data(symbol):
    symbol = symbol.upper()
    
    try:
        # Buscar dados históricos da brapi com API key
        if not symbol.endswith('.SA'):
            symbol_sa = symbol + '.SA'
        else:
            symbol_sa = symbol
            
        url = f"https://brapi.dev/api/quote/{symbol_sa}?range=3mo&interval=1d&token={BRAPI_API_KEY}"
        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            return jsonify({'error': 'Dados históricos não encontrados'}), 404
            
        data = response.json()
        if 'results' not in data or len(data['results']) == 0:
            return jsonify({'error': 'Dados históricos não encontrados'}), 404
            
        result = data['results'][0]
        historical_data = result.get('historicalDataPrice', [])
        
        if not historical_data:
            return jsonify({'error': 'Dados históricos não encontrados'}), 404
        
        chart_data = []
        for item in historical_data:
            chart_data.append({
                'date': datetime.fromtimestamp(item['date']).isoformat(),
                'open': round(float(item['open']), 2),
                'high': round(float(item['high']), 2),
                'low': round(float(item['low']), 2),
                'close': round(float(item['close']), 2),
                'volume': int(item['volume'])
            })
        
        return jsonify({
            'symbol': symbol,
            'period': '3mo',
            'interval': '1d',
            'data': chart_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar dados históricos: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.1.0',
        'platform': 'TTrader.com',
        'mobile_optimized': True
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

