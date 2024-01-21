import { Component } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';

@Component({
  selector: 'app-loja',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './loja.component.html',
  styleUrl: './loja.component.sass'
})
export class LojaComponent {
  companyUUID: string

  constructor(private route: ActivatedRoute) {
    this.companyUUID = ''
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.companyUUID = params['lojaID']
      console.log({'this.companyUUID': this.companyUUID})
    })
  }
}
