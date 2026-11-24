{% extends "base.html" %}

{% block title %}Movimentações | Stockly{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-4">
    <div>
        <h2 class="fw-bold">Movimentações de estoque</h2>
        <p class="text-muted mb-0">
            Histórico de entradas e saídas de produtos.
        </p>
    </div>

    <a href="{{ url_for('movements.create_movement') }}"
       class="btn btn-primary">
        + Nova movimentação
    </a>
</div>

<div class="card shadow-sm border-0">
    <div class="card-body">

        <div class="table-responsive">
            <table class="table table-hover align-middle">

                <thead class="table-light">
                    <tr>
                        <th>Data</th>
                        <th>Produto</th>
                        <th>Tipo</th>
                        <th>Quantidade</th>
                        <th>Responsável</th>
                        <th>Motivo</th>
                    </tr>
                </thead>

                <tbody>
                    {% for movement in movements %}
                    <tr>
                        <td>
                            {{ movement.created_at.strftime('%d/%m/%Y %H:%M') }}
                        </td>

                        <td class="fw-semibold">
                            {{ movement.product.name }}
                        </td>

                        <td>
                            {% if movement.movement_type == 'entry' %}
                                <span class="badge bg-success">
                                    Entrada
                                </span>
                            {% else %}
                                <span class="badge bg-danger">
                                    Saída
                                </span>
                            {% endif %}
                        </td>

                        <td>
                            {% if movement.movement_type == 'entry' %}
                                <span class="text-success fw-semibold">
                                    +{{ movement.quantity }}
                                </span>
                            {% else %}
                                <span class="text-danger fw-semibold">
                                    -{{ movement.quantity }}
                                </span>
                            {% endif %}
                        </td>

                        <td>
                            {{ movement.user.name }}
                        </td>

                        <td>
                            {{ movement.reason or '-' }}
                        </td>
                    </tr>

                    {% else %}
                    <tr>
                        <td colspan="6"
                            class="text-center text-muted py-4">
                            Nenhuma movimentação registrada.
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>

            </table>
        </div>

    </div>
</div>

{% endblock %}