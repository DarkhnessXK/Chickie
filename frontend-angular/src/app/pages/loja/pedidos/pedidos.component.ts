import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { FormsModule } from '@angular/forms';
import { Pedido, StatusResponse } from '../../../models/models';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';
import { ButtonHandler } from '../../../handlers/button';
import { FormatDatePipe } from '../../../pipes/format-date.pipe';

import {  CompanyAuthData, AuthService, PedidoService,
          ProdutoService, StatusService } from '../../../services/services';


@Component({
  selector: 'app-pedido',
  standalone: true,
  templateUrl: './pedidos.component.html',
  styleUrl: './pedidos.component.sass',
  imports: [
    FormatDatePipe,
    FormsModule,
    CommonModule,
    RouterModule,
    SpinnerComponent
  ]
})
export class PedidosComponent {

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
    this.route.params.subscribe(params => {

      if (!this.companyData) {
        let msg = "Dados de empresa não encontrados"
        alert(msg); throw new Error(msg)
      }

      this.statusService.getAll(this.companyData.loja.uuid).subscribe({
        next: (result: any) => {
          let payload = result.payload
          this.loading = false
          this.statusList.push(...payload)
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
            this.pedidos.value.filter(item => !item.concluido).length == 0
          )
        },
        error: (result) => {
          let msg = 'Erro na busca do pedido'
          alert(msg); console.log(result); throw new Error(msg)
        }
      })
    })
  }

  concluir(event: Event, pedido: Pedido) {
    let button = new ButtonHandler(event)
    button.disable('Concluindo...')


    this.pedidoService.concluir(pedido.uuid).subscribe({
      next: (result) => {
        button.enable()
        alert('Pedido concluído com sucesso!')

        this.ngOnInit()
      },
      error: (result) => {
        button.enable()
        alert('Erro na conclusão do pedido')
      }
    })
  }

  atualizarStatusDePedido(pedido: Pedido) {

    if (!pedido.status_uuid) {
      let msg = 'Erro ao alterar o status'
      alert(msg); throw new Error(msg)
    }

    this.pedidoService.alterarStatusDePedido(
      pedido.uuid, pedido.status_uuid
    ).subscribe({
      next: (result) => {
        alert('Status alterado com sucesso!')
      },
      error: (result) => {
        alert('Erro ao alterar o status')
      }
    })

  }

  atualizarFreteDePedido(pedido: any) {
    console.log(pedido)
    alert('Frete atualizado com sucesso!')
  }

}
