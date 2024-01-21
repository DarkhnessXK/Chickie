import { Component } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { StatusResponse, Pedido } from '../../../models/models';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CurrencyPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SpinnerComponent } from '../../../components/spinner/spinner.component';

import {  PedidoService, AuthService,
          StatusService, AuthData } from '../../../services/services';


@Component({
  selector: 'app-pedidos',
  standalone: true,
  imports: [RouterModule, CurrencyPipe, FormsModule, SpinnerComponent],
  templateUrl: './pedidos.component.html',
  styleUrl: './pedidos.component.sass'
})
export class UserPedidosComponent {
  pedidos: BehaviorSubject<Array<Pedido>>
  userData: AuthData | null
  statusList: Array<StatusResponse>
  nenhumEmAndamento: BehaviorSubject<Boolean>
  loading: boolean

  constructor(
    private pedidoService: PedidoService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private statusService: StatusService
  ) {
    this.loading = false
    this.nenhumEmAndamento = new BehaviorSubject<Boolean>(false)
    this.pedidos = new BehaviorSubject<Array<Pedido>>([])
    this.statusList = []
    this.userData = this.authService.currentUser()
  }

  ngOnInit() {
    this.loading = true

    if (!this.userData || !this.userData.uuid) {
      let msg = 'Dados de usuário não encontrados!'
      alert(msg); throw new Error(msg)
    }

    this.pedidoService.getAllFromUser(this.userData.uuid).subscribe({
      next: (response: any) => {
        let payload = response.payload
        this.loading = false
        this.pedidos.next(payload)
        this.nenhumEmAndamento.next(
          this.pedidos.value.filter(item => !item.concluido).length == 0
        )
      },
      error: (response) => {
        let msg = 'Erro na busca do pedido'
        alert(msg); console.log(response); throw new Error(msg)
      }
    })
  }
}
