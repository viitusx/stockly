{% extends "base.html" %}

{% block title %}Nova Movimentação | Stockly{% endblock %}

{% block content %}

<div class="mb-4">
    <h2 class="fw-bold">Nova movimentação</h2>
    <p class="text-muted">
        Registre entradas ou saídas de produtos do estoque.
    </p>
</div>

<div class="card shadow-sm border-0">
    <div class="card-body p-4">

        {% if products %}

        <form method="POST">

            <div class="mb-3">
                <label for="product_id" class="form-label">
                    Produto *
                </label>

                <select
                    class="form-select"
                    id="product_id"
                    name="product_id"
                    required
                >
                    <option value="">Selecione um produto</option>

                    {% for product in products %}
                    <option value="{{ product.id }}">
                        {{ product.name }} — SKU: {{ product.sku }}
                        (Estoque: {{ product.quantity }})
                    </option>
                    {% endfor %}
                </select>
            </div>

            <div class="mb-3">
                <label for="movement_type" class="form-label">
                    Tipo de movimentação *
                </label>

                <select
                    class="form-select"
                    id="movement_type"
                    name="movement_type"
                    required
                >
                    <option value="">Selecione o tipo</option>
                    <option value="entry">Entrada de estoque</option>
                    <option value="exit">Saída de estoque</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="quantity" class="form-label">
                    Quantidade *
                </label>

                <input
                    type="number"
                    class="form-control"
                    id="quantity"
                    name="quantity"
                    min="1"
                    step="1"
                    placeholder="Ex: 10"
                    required
                >
            </div>

            <div class="mb-4">
                <label for="reason" class="form-label">
                    Motivo da movimentação
                </label>

                <textarea
                    class="form-control"
                    id="reason"
                    name="reason"
                    rows="3"
                    maxlength="255"
                    placeholder="Ex: Compra de mercadorias ou venda de produtos."
                ></textarea>
            </div>

            <div class="alert alert-info">
                <strong>Atenção:</strong>
                as saídas só serão permitidas quando houver quantidade
                suficiente disponível no estoque.
            </div>

            <div class="d-flex gap-2">

                <button type="submit" class="btn btn-primary">
                    Registrar movimentação
                </button>

                <a href="{{ url_for('movements.list_movements') }}"
                   class="btn btn-outline-secondary">
                    Cancelar
                </a>

            </div>

        </form>

        {% else %}

        <div class="alert alert-warning mb-3">
            Nenhum produto ativo cadastrado.
            Cadastre um produto antes de registrar movimentações.
        </div>

        <a href="{{ url_for('products.create_product') }}"
           class="btn btn-primary">
            Cadastrar produto
        </a>

        {% endif %}

    </div>
</div>

{% endblock %}