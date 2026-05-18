import trainer
import threads

if __name__ == '__main__':
    X_train, X_test, y_train, y_test, X_val, y_val = trainer.cargar_dataset()

    # Regresion lineal
    trainer.regresion_lineal(X_train, y_train, X_test, y_test)

    # Red neuronal
    model = trainer.construir_modelo(X_train.shape[1])
    trainer.entrenar_modelo(model, X_train, y_train, X_test, y_test)
    trainer.guardar_modelo(model)

    # Evaluacion con test set
    test_loss, test_mse, test_mae, test_r2 = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test — Loss: {test_loss:.4f} | MSE: {test_mse:.4f} | MAE: {test_mae:.4f} | R²: {test_r2:.4f}")

    # Evaluacion con val set
    val_loss, val_mse, val_mae, val_r2 = model.evaluate(X_val, y_val, verbose=0)
    print(f"Val  — Loss: {val_loss:.4f} | MSE: {val_mse:.4f} | MAE: {val_mae:.4f} | R²: {val_r2:.4f}")

    # Prediccion batch sobre val set
    preds_val = threads.predecir_batch(X_val.values.tolist())
    print("\nPredicciones batch (val set):")
    for i, (pred, real) in enumerate(zip(preds_val, y_val.tolist())):
        print(f"  [{i}] Predicho: {pred:.4f} | Real: {real:.4f}")

