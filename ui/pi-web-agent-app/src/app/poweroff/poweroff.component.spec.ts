import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PoweroffComponent } from './poweroff.component';

describe('PoweroffComponent', () => {
  let component: PoweroffComponent;
  let fixture: ComponentFixture<PoweroffComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PoweroffComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PoweroffComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
