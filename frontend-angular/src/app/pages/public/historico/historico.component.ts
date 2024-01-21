import { Component } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Pedido, StatusResponse } from '../../../models/models';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CurrencyPipe, NgStyle } from '@angular/common';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';
import { FormatDatePipe } from '../../../pipes/format-date.pipe';

import {  AuthData, PedidoService, ProdutoService,
          StatusService, AuthService } from '../../../services/services';


@Component({
  selector: 'app-historico',
  standalone: true,
  imports: [
    FormatDatePipe,
    RouterModule,
    CurrencyPipe,
    NgStyle,
    SpinnerComponent
  ],
  templateUrl: './historico.component.html',
  styleUrl: './historico.component.sass'
})
export class UserHistoricoComponent {

  pedidoUUID: string
  pedidos: BehaviorSubject<Array<Pedido>>
  statusList: Array<StatusResponse>
  nenhumEmAndamento: BehaviorSubject<Boolean>
  loading: boolean
  userData: AuthData | null

  constructor(
    private pedidoService: PedidoService,
    private produtoService: ProdutoService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private statusService: StatusService
  ) {
    this.userData = null
    this.loading = false
    this.nenhumEmAndamento = new BehaviorSubject<Boolean>(false)
    this.pedidos = new BehaviorSubject<Array<Pedido>>([])
    this.statusList = []
    this.pedidoUUID = ''
  }


  ngOnInit() {
    this.loading = true
    this.userData = this.authService.currentUser()

    if (!this.userData) {
      let msg = "Dados de usuario não encontrados"
      alert(msg); throw new Error(msg)
    }

    this.pedidoService.getAllFromUser(this.userData.uuid).subscribe({
      next: (result: any) => {
        let payload = result.payload
        this.loading = false
        this.pedidos.next(payload)
        this.nenhumEmAndamento.next(
          this.pedidos.value.filter(item => item.concluido).length == 0
        )
      },
      error: (result) => {
        let msg = 'Erro na busca do pedido'
        alert(msg); console.log(result); throw new Error(msg)
      }
    })
  }

}
