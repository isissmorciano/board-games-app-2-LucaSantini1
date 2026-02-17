from flask import request, jsonify, render_template
from . import app
from .db import get_db


@app.route('/giochi', methods=['POST'])
def create_gioco():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    required = ['nome', 'numero_giocatori_massimo', 'durata_media', 'categoria']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields', 'required': required}), 400

    try:
        numero = int(data['numero_giocatori_massimo'])
        durata = int(data['durata_media'])
    except (ValueError, TypeError):
        return jsonify({'error': 'numero_giocatori_massimo and durata_media must be integers'}), 400

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            'INSERT INTO giochi (nome, numero_giocatori_massimo, durata_media, categoria) VALUES (?, ?, ?, ?)',
            (data['nome'], numero, durata, data['categoria'])
        )
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/giochi', methods=['GET'])
def list_giochi():
    conn = get_db()
    giochi = conn.execute('SELECT * FROM giochi').fetchall()
    conn.close()
    return jsonify([dict(g) for g in giochi])


@app.route('/')
def index():
    """Serve una semplice UI HTML che usa le API JSON."""
    return render_template('index.html')


@app.route('/ui/giochi')
def ui_giochi():
    return render_template('giochi.html')


@app.route('/ui/giochi/<int:gioco_id>/partite')
def ui_partite(gioco_id):
    return render_template('partite.html', gioco_id=gioco_id)


@app.route('/giochi/<int:gioco_id>/partite', methods=['POST'])
def create_partita(gioco_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON payload'}), 400

    required = ['data', 'vincitore', 'punteggio_vincitore']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields', 'required': required}), 400

    try:
        punteggio = int(data['punteggio_vincitore'])
    except (ValueError, TypeError):
        return jsonify({'error': 'punteggio_vincitore must be an integer'}), 400

    conn = get_db()
    # verify game exists
    gioco = conn.execute('SELECT id FROM giochi WHERE id = ?', (gioco_id,)).fetchone()
    if gioco is None:
        conn.close()
        return jsonify({'error': 'Gioco non trovato'}), 404

    try:
        c = conn.cursor()
        c.execute(
            'INSERT INTO partite (gioco_id, data, vincitore, punteggio_vincitore) VALUES (?, ?, ?, ?)',
            (gioco_id, data['data'], data['vincitore'], punteggio)
        )
        conn.commit()
        new_id = c.lastrowid
        conn.close()
        return jsonify({'success': True, 'id': new_id}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/giochi/<int:gioco_id>/partite', methods=['GET'])
def list_partite(gioco_id):
    conn = get_db()
    # verify game exists
    gioco = conn.execute('SELECT id FROM giochi WHERE id = ?', (gioco_id,)).fetchone()
    if gioco is None:
        conn.close()
        return jsonify({'error': 'Gioco non trovato'}), 404
    partite = conn.execute('SELECT * FROM partite WHERE gioco_id = ?', (gioco_id,)).fetchall()
    conn.close()
    return jsonify([dict(p) for p in partite])
