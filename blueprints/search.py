from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from database.master_contract_db import search_symbols

search_bp = Blueprint('search_bp', __name__, url_prefix='/search')

@search_bp.route('/token')
def token():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))  # Fixed auth_bp.login to auth.login
    return render_template('token.html')

@search_bp.route('/')
def search():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))  # Fixed auth_bp.login to auth.login
    
    symbol = request.args.get('symbol')
    exchange = request.args.get('exchange')
    
    # If no search params, just render the page
    if not symbol:
        return render_template('search.html')
    
    results = search_symbols(symbol, exchange)
    
    # Check if this is an API/AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        if not results:
            return jsonify({'status': 'success', 'results': []})
        else:
            results_dicts = [{
                'symbol': result.symbol,
                'brsymbol': result.brsymbol,
                'name': result.name,
                'exchange': result.exchange,
                'brexchange': result.brexchange,
                'token': result.token,
                'expiry': result.expiry,
                'strike': result.strike,
                'lotsize': result.lotsize,
                'instrumenttype': result.instrumenttype,
                'tick_size': result.tick_size
            } for result in results]
            return jsonify({'status': 'success', 'results': results_dicts})
    else:
        # For browser requests, render template with results
        return render_template('search.html', results=results, symbol=symbol, exchange=exchange)

# New endpoint for autocomplete suggestions
@search_bp.route('/suggestions')
def get_suggestions():
    if not session.get('logged_in'):
        return jsonify([])
    
    symbol = request.args.get('term', '')  # 'term' is common for jQuery autocomplete
    exchange = request.args.get('exchange', 'NSE')
    
    if not symbol or len(symbol) < 1:
        return jsonify([])
        
    results = search_symbols(symbol, exchange)
    
    # Format suggestions as a list of items
    suggestions = [{
        'label': f"{result.symbol} - {result.name}",
        'value': result.symbol,
        'token': result.token,
        'exchange': result.exchange
    } for result in results[:10]]  # Limit to 10 suggestions
    
    return jsonify(suggestions)