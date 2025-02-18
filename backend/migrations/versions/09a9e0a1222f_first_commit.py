"""first_commit

Revision ID: 09a9e0a1222f
Revises: 
Create Date: 2024-01-07 04:34:28.442811

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09a9e0a1222f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enderecos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('uf', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='uf'), nullable=True),
    sa.Column('cidade', sa.Text(), nullable=False),
    sa.Column('logradouro', sa.Text(), nullable=False),
    sa.Column('numero', sa.Text(), nullable=True),
    sa.Column('complemento', sa.Text(), nullable=True),
    sa.Column('bairro', sa.Text(), nullable=False),
    sa.Column('cep', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('lojas',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('telefone', sa.Text(), nullable=True),
    sa.Column('celular', sa.Text(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('horarios_de_funcionamento', sa.Text(), nullable=True),
    sa.Column('passou_pelo_primeiro_acesso', sa.Boolean(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('celular'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('usuarios',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('telefone', sa.Text(), nullable=True),
    sa.Column('celular', sa.Text(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('passou_pelo_primeiro_acesso', sa.Boolean(), nullable=True),
    sa.Column('modo_de_cadastro', sa.Enum('importacao', 'cadastro_de_loja', 'auto_cadastro', name='modo_de_cadastro'), nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('celular'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('avaliacoes_de_loja',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('usuario_uuid', sa.String(length=36), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('nota', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.ForeignKeyConstraint(['usuario_uuid'], ['usuarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('categorias_de_produtos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('loja_uuid', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('clientes',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=True),
    sa.Column('usuario_uuid', sa.String(length=36), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.ForeignKeyConstraint(['usuario_uuid'], ['usuarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('enderecos_lojas',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('uf', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='uf'), nullable=True),
    sa.Column('cidade', sa.Text(), nullable=False),
    sa.Column('logradouro', sa.Text(), nullable=False),
    sa.Column('numero', sa.Text(), nullable=True),
    sa.Column('complemento', sa.Text(), nullable=True),
    sa.Column('bairro', sa.Text(), nullable=False),
    sa.Column('cep', sa.Text(), nullable=True),
    sa.Column('loja_uuid', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('enderecos_usuarios',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('uf', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='uf'), nullable=True),
    sa.Column('cidade', sa.Text(), nullable=False),
    sa.Column('logradouro', sa.Text(), nullable=False),
    sa.Column('numero', sa.Text(), nullable=True),
    sa.Column('complemento', sa.Text(), nullable=True),
    sa.Column('bairro', sa.Text(), nullable=False),
    sa.Column('cep', sa.Text(), nullable=True),
    sa.Column('usuario_uuid', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['usuario_uuid'], ['usuarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('entregadores',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('telefone', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('celular', sa.Text(), nullable=True),
    sa.Column('veiculo', sa.Text(), nullable=True),
    sa.Column('placa_veiculo', sa.Text(), nullable=True),
    sa.Column('loja_uuid', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('nome'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('funcionarios',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('cargo', sa.Text(), nullable=True),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('telefone', sa.Text(), nullable=True),
    sa.Column('celular', sa.Text(), nullable=True),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('metodos_pagamento',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('Descricao', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('status',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('zonas_de_entrega',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('cidade', sa.Text(), nullable=True),
    sa.Column('uf', sa.Text(), nullable=True),
    sa.Column('bairro', sa.Text(), nullable=True),
    sa.Column('taxa_de_entrega', sa.Float(), nullable=True),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('pedidos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('data_hora', sa.DateTime(), nullable=True),
    sa.Column('status_uuid', sa.String(length=36), nullable=True),
    sa.Column('frete', sa.Float(), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('celular', sa.String(length=20), nullable=False),
    sa.Column('usuario_uuid', sa.String(length=36), nullable=True),
    sa.Column('concluido', sa.Boolean(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.ForeignKeyConstraint(['status_uuid'], ['status.uuid'], ),
    sa.ForeignKeyConstraint(['usuario_uuid'], ['usuarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('produtos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('nome', sa.Text(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.Column('categoria_uuid', sa.String(length=36), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['categoria_uuid'], ['categorias_de_produtos.uuid'], ),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('avaliacoes_de_produtos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('usuario_uuid', sa.String(length=36), nullable=False),
    sa.Column('loja_uuid', sa.String(length=36), nullable=False),
    sa.Column('produto_uuid', sa.String(length=36), nullable=False),
    sa.Column('nota', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.ForeignKeyConstraint(['produto_uuid'], ['produtos.uuid'], ),
    sa.ForeignKeyConstraint(['usuario_uuid'], ['usuarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('enderecos_entregas',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('uf', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='uf'), nullable=True),
    sa.Column('cidade', sa.Text(), nullable=False),
    sa.Column('logradouro', sa.Text(), nullable=False),
    sa.Column('numero', sa.Text(), nullable=True),
    sa.Column('complemento', sa.Text(), nullable=True),
    sa.Column('bairro', sa.Text(), nullable=False),
    sa.Column('cep', sa.Text(), nullable=True),
    sa.Column('pedido_uuid', sa.Text(), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['pedido_uuid'], ['pedidos.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('itens_pedido',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.Column('observacoes', sa.Text(), nullable=True),
    sa.Column('produto_uuid', sa.String(length=36), nullable=True),
    sa.Column('pedido_uuid', sa.String(length=36), nullable=True),
    sa.Column('loja_uuid', sa.String(length=36), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['loja_uuid'], ['lojas.uuid'], ),
    sa.ForeignKeyConstraint(['pedido_uuid'], ['pedidos.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['produto_uuid'], ['produtos.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('pagamentos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('pedido_uuid', sa.String(length=36), nullable=False),
    sa.Column('metodo_pagamento_uuid', sa.String(length=36), nullable=False),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['metodo_pagamento_uuid'], ['metodos_pagamento.uuid'], ),
    sa.ForeignKeyConstraint(['pedido_uuid'], ['pedidos.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('precos',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('produto_uuid', sa.String(length=36), nullable=False),
    sa.Column('valor', sa.Float(), nullable=True),
    sa.Column('dia_da_semana', sa.Enum('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom', name='diasdasemana'), nullable=True),
    sa.Column('ativo', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['produto_uuid'], ['produtos.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('precos')
    op.drop_table('pagamentos')
    op.drop_table('itens_pedido')
    op.drop_table('enderecos_entregas')
    op.drop_table('avaliacoes_de_produtos')
    op.drop_table('produtos')
    op.drop_table('pedidos')
    op.drop_table('zonas_de_entrega')
    op.drop_table('status')
    op.drop_table('metodos_pagamento')
    op.drop_table('funcionarios')
    op.drop_table('entregadores')
    op.drop_table('enderecos_usuarios')
    op.drop_table('enderecos_lojas')
    op.drop_table('clientes')
    op.drop_table('categorias_de_produtos')
    op.drop_table('avaliacoes_de_loja')
    op.drop_table('usuarios')
    op.drop_table('lojas')
    op.drop_table('enderecos')
    # ### end Alembic commands ###
