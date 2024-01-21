import { Routes } from '@angular/router';
import { LojaHomeComponent } from '../pages/loja/home/home.component';
import { CadastroCategoriaComponent } from '../pages/loja/cadastro-categoria/cadastro-categoria.component';
import { ProdutosComponent } from '../pages/loja/produtos/produtos.component';
import { CategoriaComponent } from '../pages/loja/categoria/categoria.component';
import { ProdutoComponent } from '../pages/loja/produto/produto.component';
import { PedidosComponent } from '../pages/loja/pedidos/pedidos.component';
import { StatusComponent } from '../pages/loja/status/status.component';
import { companyAuthGuard } from '../guards/company-auth.guard';
import { LojaSettingsComponent } from '../pages/loja/loja-settings/loja-settings.component';
import { SignupLojaComponent } from '../pages/loja/signup-loja/signup-loja.component';
import { PedidoComponent } from '../pages/public/pedido/pedido.component';
import { HistoricoComponent } from '../pages/loja/historico/historico.component';
import { CadastroClienteComponent } from '../pages/loja/cadastro-cliente/cadastro-cliente.component';
import { ClientesComponent } from '../pages/loja/clientes/clientes.component';
import { CadastrarPedidoComponent } from '../pages/loja/cadastrar-pedido/cadastrar-pedido.component';


export const lojaRoutes: Routes = [

  { path: 'loja/settings',
    component: LojaSettingsComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/cadastrar-pedido',
    component: CadastrarPedidoComponent },

  { path: 'loja/cadastro-cliente',
    component: CadastroClienteComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/pedidos/:pedidoID',
    component: PedidoComponent,
    canActivate: [companyAuthGuard] },

  { path: 'signup/loja',
    component: SignupLojaComponent },

  { path: 'loja/home',
    component: LojaHomeComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/categorias',
    component: CadastroCategoriaComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/categorias/:id',
    component: CategoriaComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/produtos/:id',
    component: ProdutoComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/produtos',
    component: ProdutosComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/pedidos',
    component: PedidosComponent,
    canActivate: [companyAuthGuard] },

    { path: 'loja/historico',
    component: HistoricoComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/status',
    component: StatusComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/clientes',
    component: ClientesComponent,
    canActivate: [companyAuthGuard] },
];
