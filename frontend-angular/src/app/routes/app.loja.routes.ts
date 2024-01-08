import { Routes } from '@angular/router';
import { LojaHomeComponent } from '../pages/loja/home/home.component';
import { CadastroCategoriaComponent } from '../pages/loja/cadastro-categoria/cadastro-categoria.component';
import { CadastroProdutoComponent } from '../pages/loja/cadastro-produto/cadastro-produto.component';
import { CategoriaComponent } from '../pages/loja/categoria/categoria.component';
import { ProdutoComponent } from '../pages/loja/produto/produto.component';
import { PedidosComponent } from '../pages/loja/pedidos/pedidos.component';
import { StatusComponent } from '../pages/loja/status/status.component';
import { companyAuthGuard } from '../guards/company-auth.guard';
import { LojaSettingsComponent } from '../pages/loja/loja-settings/loja-settings.component';
import { SignupLojaComponent } from '../pages/loja/signup-loja/signup-loja.component';
import { PedidoComponent } from '../pages/public/pedido/pedido.component';


export const lojaRoutes: Routes = [

  { path: 'loja/settings',
    component: LojaSettingsComponent,
    canActivate: [companyAuthGuard]},

  { path: 'loja/pedidos/:pedidoID',
    component: PedidoComponent,
    canActivate: [companyAuthGuard]},

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
    component: CadastroProdutoComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/pedidos',
    component: PedidosComponent,
    canActivate: [companyAuthGuard] },

  { path: 'loja/status',
    component: StatusComponent,
    canActivate: [companyAuthGuard] },

];
