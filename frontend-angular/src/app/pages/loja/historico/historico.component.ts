import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { Pedido, StatusResponse } from '../../../models/models';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';
import { FormatDatePipe } from '../../../pipes/format-date.pipe';
import { CurrencyPipe } from '@angular/common';

import {  CompanyAuthData, AuthService, PedidoService,
          ProdutoService, StatusService } from '../../../services/services';


@Component({
  selector: 'app-pedido',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    RouterModule,
    SpinnerComponent,
    FormatDatePipe,
    CurrencyPipe
  ],
  templateUrl: './historico.component.html',
  styleUrl: './historico.component.sass'
})
export class HistoricoComponent {

  total: number = 0
  pedidoUUID: string
  pedidos: BehaviorSubject<Array<Pedido>>
  companyData: CompanyAuthData | null
  statusList: Array<StatusResponse>
  nenhumEmAndamento: BehaviorSubject<Boolean>
  loading: boolean

  constructor(
    private pedidoService: PedidoService,
    private produtoService: ProdutoService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private statusService: StatusService
  ) {
    this.loading = false
    this.nenhumEmAndamento = new BehaviorSubject<Boolean>(false)
    this.pedidos = new BehaviorSubject<Array<Pedido>>([])
    this.statusList = []
    this.pedidoUUID = ''
    this.companyData = this.authService.currentCompany()
  }

  ngOnInit() {
    this.loading = true

    if (!this.companyData) {
      let msg = "Dados de empresa não encontrados"
      alert(msg); throw new Error(msg)
    }

    this.statusService.getAll(this.companyData.loja.uuid).subscribe({
      next: (result: any) => {
        this.loading = false
        this.statusList.push(...result)
      },
      error: (result) => {
        throw new Error('Erro na requisição dos dados')
      }
    })

    this.pedidoService.getAll(this.companyData.loja.uuid).subscribe({
      next: (result: any) => {
        let payload = result.payload
        this.pedidos.next(payload)
        this.nenhumEmAndamento.next(
          this.pedidos.value.filter(item => item.concluido).length == 0
        )

          for (let pedido of payload) {
            for (let item of pedido.itens) {
              this.total += (item.quantidade * item.valor)
            }
          }

      },
      error: (result) => {
        let msg = 'Erro na busca do pedido'
        alert(msg); console.log(result); throw new Error(msg)
      }
    })

  }

}
