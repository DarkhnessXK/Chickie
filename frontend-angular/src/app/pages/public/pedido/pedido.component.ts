import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BehaviorSubject } from 'rxjs';
import { Pedido } from '../../../models/models';
import { PedidoService, ProdutoService } from '../../../services/services';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormatDatePipe } from '../../../pipes/format-date.pipe';


@Component({
  selector: 'app-pedido',
  standalone: true,
  imports: [CommonModule, RouterModule, FormatDatePipe],
  templateUrl: './pedido.component.html',
  styleUrl: './pedido.component.sass'
})
export class PedidoComponent {

  pedidoUUID: string | null
  pedido: Pedido | null
  total: BehaviorSubject<number>
  thisURL: string

  constructor(
    private pedidoService: PedidoService,
    private produtoService: ProdutoService,
    private route: ActivatedRoute
  ) {
    this.pedido = null
    this.pedidoUUID = null
    this.total = new BehaviorSubject<number>(0)
    this.thisURL = String(window.location.pathname)
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.pedidoUUID = params['pedidoID']
      if (!this.pedidoUUID) {
        let msg = 'ID do pedido nao encontrado!'
        alert(msg); throw new Error(msg)
      }
      this.pedidoService.getOne(this.pedidoUUID).subscribe({
        next: (response: any) => {
          this.pedido = {...response}
          this.fetchProducts()
        },
        error: (response) => {
          let msg = 'Erro na busca do pedido'
          alert(msg); console.log(response); throw new Error(msg)
        }
      })
    })
  }


  fetchProducts() {
    if (!this.pedido) {
      let msg = 'Erro na requisição dos dados'
      alert(msg); throw new Error(msg)
    }
    for (let item of this.pedido.itens) {
        item.subtotal = Number(item.quantidade * item.valor)
        this.total.next(this.total.getValue() + item.subtotal)
    }
  }

}
